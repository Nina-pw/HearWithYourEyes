import sounddevice as sd
import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt

# ===== ตั้งค่า =====
DURATION = 2      # อัดเสียง 2 วินาที
SR = 16000       # sample rate (เหมือนที่ YAMNet ใช้)

print("🎤 Recording from ReSpeaker...")
audio = sd.rec(int(DURATION * SR), samplerate=SR, channels=1, dtype="float32")
sd.wait()
audio = audio.flatten()

print("Creating Mel Spectrogram...")

mel = librosa.feature.melspectrogram(
    y=audio,
    sr=SR,
    n_mels=64,
    n_fft=1024,
    hop_length=320
)

mel_db = librosa.power_to_db(mel, ref=np.max)

plt.figure(figsize=(10, 4))
librosa.display.specshow(
    mel_db,
    sr=SR,
    hop_length=320,
    x_axis="time",
    y_axis="mel"
)
plt.colorbar(format="%+2.0f dB")
plt.title("Mel Spectrogram from ReSpeaker 2-Mic")
plt.tight_layout()
plt.savefig("mel_spectrogram.png", dpi=300)
print("Saved mel_spectrogram.png")

# python mel_view.py
# scp pi@project492:~/mel_spectrogram.png .


