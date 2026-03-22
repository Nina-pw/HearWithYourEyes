import os
import csv
import argparse
import time
import numpy as np
from collections import deque

from tflite_runtime.interpreter import Interpreter
from yeelight import Bulb
import requests

# =========================
# Home Assistant Webhook
# =========================
HA_WEBHOOK_URL = "http://192.168.1.104:8123/api/webhook/yamnet_event"

def send_to_home_assistant(event_name, confidence, color_name=None):
    payload = {
        "event": event_name,
        "confidence": float(confidence),
        "color": color_name or "Unknown",
    }
    try:
        requests.post(HA_WEBHOOK_URL, json=payload, timeout=2)
        print(f"📡 Sent to Home Assistant → {payload}")
    except Exception as e:
        print(f"⚠️ Error sending to Home Assistant: {e}")

# =========================
# CLI
# =========================
p = argparse.ArgumentParser(description="Detect sound events using YAMNet + Yeelight (Final Balanced + Fail-safe)")
p.add_argument("--mic", action="store_true")
p.add_argument("--duration", type=float, default=1.0)
p.add_argument("--device", type=int, default=None)
p.add_argument("--loop", action="store_true")
p.add_argument("--topk", "-k", type=int, default=5)
args = p.parse_args()

USE_MIC = args.mic
MIC_DURATION = args.duration
MIC_DEVICE = args.device
MIC_LOOP = args.loop
TOPK = args.topk

MODEL = "yamnet.tflite"
CLASS_MAP = "yamnet_class_map.csv"

# =========================
# Load model & class map
# =========================
if not os.path.isfile(MODEL):
    raise FileNotFoundError(f"Model file not found: {MODEL}")
if not os.path.isfile(CLASS_MAP):
    raise FileNotFoundError(f"Class map CSV not found: {CLASS_MAP}")

idx2name = {}
with open(CLASS_MAP, newline='', encoding='utf-8') as f:
    for row in csv.DictReader(f):
        idx2name[int(row['index'])] = row['display_name']

interp = Interpreter(model_path=MODEL)
interp.allocate_tensors()
in_details = interp.get_input_details()[0]
outs = interp.get_output_details()
in_idx = in_details["index"]
in_shape = in_details["shape"]
expected_len = int(in_shape[-1])
print(f"Interpreter ready. input shape: {in_shape}, expected waveform length: {expected_len}")

# =========================
# Yeelight
# =========================
BULB_IP = "192.168.1.103"
bulb = Bulb(BULB_IP)

def blink_bulb(bulb, color, times=3, duration=0.4,
               fallback_color=(200, 200, 200), fallback_brightness=20):
    try:
        bulb.turn_on()
        for _ in range(times):
            bulb.set_rgb(*color)
            bulb.set_brightness(100)
            time.sleep(duration)
            bulb.set_rgb(*fallback_color)
            bulb.set_brightness(fallback_brightness)
            time.sleep(duration)
    except Exception as e:
        print(f"⚠️ Yeelight error: {e}")

# =========================
# Event → Color
# =========================
EVENT_COLOR_MAP = {
    "smoke alarm": (255, 0, 0),
    "fire alarm": (255, 0, 0),
    "carbon monoxide alarm": (255, 0, 0),
    "gas": (255, 0, 0),
    "gunshot, gunfire": (255, 0, 0),
    "explosion": (255, 0, 0),
    "siren": (255, 0, 0),
    "car alarm": (255, 0, 0),
    "air horn": (255, 0, 0),
    "alarm": (255, 0, 0),
    "alarm clock": (255, 0, 0),

    "glass": (255, 165, 0),
    "glass breaking": (255, 165, 0),
    "impact": (255, 165, 0),

    "scream": (255, 255, 0),
    "shout": (255, 255, 0),
    "kettle whistle": (255, 255, 0),
    "whistle": (255, 255, 0),

    "telephone bell ringing": (0, 255, 0),
    "doorbell": (0, 255, 0),
    "knock": (0, 255, 0),
    "ringtone": (0, 255, 0),

    "baby cry, infant cry": (0, 170, 255),
    "dog": (0, 170, 255),
    "bark": (0, 170, 255),
}

COLOR_NAME_MAP = {
    (255, 0, 0): "Red",
    (255, 165, 0): "Orange",
    (255, 255, 0): "Yellow",
    (0, 255, 0): "Green",
    (0, 170, 255): "Cyan",
}
NAME_TO_RGB = {v: k for k, v in COLOR_NAME_MAP.items()}
COLOR_PRIORITY = {"Red": 1, "Orange": 2, "Yellow": 3, "Green": 4, "Cyan": 5}

COLOR_THRESHOLD = {"Red": 0.4, "Orange": 0.20, "Yellow": 0.18, "Green": 0.12, "Cyan": 0.07}

# =========================
# Audio utils
# =========================
def record_mic_16k(duration=1.0, device=None):
    n_samples = int(16000 * duration)
    import sounddevice as sd
    audio = sd.rec(frames=n_samples, samplerate=16000, channels=1, dtype="float32", device=device)
    sd.wait()
    return audio.flatten(), 16000

def compute_rms(wav):
    return float(np.sqrt(np.mean(np.square(wav))))

def normalize_audio(wav, target_rms=0.1):
    rms = compute_rms(wav)
    if rms < 1e-6:
        return wav
    gain = target_rms / rms
    return np.clip(wav * gain, -1.0, 1.0)

# =========================
# Dynamic threshold
# =========================
NOISE_FLOOR = None
CURRENT_RMS = 0.0

def dynamic_threshold(base_thresh, rms, noise_floor, cname):
    if cname == "Red":
        scale = np.clip(rms / (noise_floor + 1e-6), 0.7, 1.05)
    else:
        scale_map = {
            "Orange": (0.75, 1.2),
            "Yellow": (0.85, 1.5),
            "Green": (0.8, 1.6),
            "Cyan": (0.8, 1.8),
        }
        lo, hi = scale_map[cname]
        scale = np.clip(rms / (noise_floor + 1e-6), lo, hi)

    return np.clip(base_thresh * scale, 0.03, 0.9)

# =========================
# Prediction
# =========================
def prepare_input(wav):
    if len(wav) > expected_len:
        wav2 = wav[-expected_len:]
    else:
        wav2 = np.pad(wav, (expected_len - len(wav), 0), mode='constant')
    return wav2.astype(np.float32)

def get_scores2d_from_interpreter(interp, outs):
    for od in outs:
        out = interp.get_tensor(od['index'])
        if out.ndim == 3:
            return out[0]
        if out.ndim == 2:
            return out
    out0 = interp.get_tensor(outs[0]['index'])
    return out0[np.newaxis, :]

def predict_topk(wav, k=5):
    inp = prepare_input(wav)
    try:
        interp.set_tensor(in_idx, inp)
    except:
        interp.set_tensor(in_idx, np.reshape(inp, in_shape))
    interp.invoke()
    scores2d = get_scores2d_from_interpreter(interp, outs)
    agg = scores2d.max(axis=0)
    top_idxs = np.argsort(agg)[::-1][:k]
    return [(idx2name.get(int(i), f"cls_{i}"), float(agg[int(i)])) for i in top_idxs]

# =========================
# Decision Logic
# =========================
def pick_priority_color(topk):
    passed = []
    emergency_hit = None

    for lab, score in topk:
        ll = lab.lower()
        for key, rgb in EVENT_COLOR_MAP.items():
            if key in ll:
                cname = COLOR_NAME_MAP[rgb]
                base = COLOR_THRESHOLD.get(cname, 0.1)
                dyn = dynamic_threshold(base, CURRENT_RMS, NOISE_FLOOR, cname)

                if cname == "Red":
                    if any(k in ll for k in ["fire alarm", "smoke", "siren"]):
                        dyn *= 0.65
                    elif any(k in ll for k in ["car alarm", "air horn"]):
                        dyn *= 0.8
                    elif "buzzer" in ll:
                        dyn *= 0.9

                if cname == "Orange" and any(k in ll for k in ["glass", "impact"]):
                    dyn *= 0.75

                if score >= dyn:
                    item = {"label": lab, "color": cname, "score": score, "priority": COLOR_PRIORITY[cname]}
                    passed.append(item)
                    if cname == "Red":
                        emergency_hit = item
                break

    if emergency_hit:
        return emergency_hit["color"], [(emergency_hit["label"], emergency_hit["score"])]

    if not passed:
        return None

    min_p = min(x["priority"] for x in passed)
    same = [x for x in passed if x["priority"] == min_p]
    best = max(same, key=lambda x: x["score"])
    return best["color"], [(best["label"], best["score"])]

# =========================
# Cooldown
# =========================
LAST_EVENT_TIME = {}
EVENT_COOLDOWN = {"Red": 5, "Orange": 8, "Yellow": 10, "Green": 20, "Cyan": 20}

def can_trigger(event_name, color, conf):
    now = time.time()
    last = LAST_EVENT_TIME.get(event_name, 0)
    cooldown = EVENT_COOLDOWN[color]
    if now - last > cooldown or conf > 0.85:
        LAST_EVENT_TIME[event_name] = now
        return True
    return False

# =========================
# MAIN
# =========================
if USE_MIC:
    print(f"🎤 MIC mode: duration={MIC_DURATION}s device={MIC_DEVICE} loop={MIC_LOOP}")
    try:
        round_i = 0
        NOISE_ALPHA = 0.95

        while True:
            round_i += 1
            wav, sr = record_mic_16k(MIC_DURATION, device=MIC_DEVICE)

            rms = compute_rms(wav)
            CURRENT_RMS = rms

            if NOISE_FLOOR is None:
                NOISE_FLOOR = rms
                print(f"🎯 Init noise floor = {NOISE_FLOOR:.4f}")
            else:
                if rms < NOISE_FLOOR * 1.01:
                    NOISE_FLOOR = NOISE_ALPHA * NOISE_FLOOR + (1 - NOISE_ALPHA) * rms
                NOISE_FLOOR = min(NOISE_FLOOR, 0.6)

            print(f"🔊 RMS = {rms:.4f} | Noise floor = {NOISE_FLOOR:.4f}")

            if rms < NOISE_FLOOR + 0.0003:
                print("🤫 Too quiet → skip")
                continue

            wav = normalize_audio(wav)

            topk = predict_topk(wav, k=TOPK)
            print(f"[MIC {round_i}] => " + ", ".join([f"{lab}:{sc:.3f}" for lab, sc in topk]))

            choice = pick_priority_color(topk)

            if choice:
                cname, items = choice
                event_name, conf = items[0]
                if can_trigger(event_name, cname, conf):
                    print(f"⚡ Detected {event_name} ({conf:.2f}) → Blink {cname}")
                    send_to_home_assistant(event_name, conf, cname)
                    blink_bulb(bulb, NAME_TO_RGB[cname])
                else:
                    print("⏳ Cooldown active → skip")
            else:
                print("⚡ No stable event")

            if not MIC_LOOP:
                break

    except KeyboardInterrupt:
        print("\n🛑 Stopped.")