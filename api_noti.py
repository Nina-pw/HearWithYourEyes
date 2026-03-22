from fastapi import FastAPI
from dotenv import load_dotenv
import os
import requests
from datetime import datetime
from time import time

load_dotenv()

LINE_TOKEN = os.getenv("LINE_TOKEN")
LINE_USER_ID = os.getenv("LINE_USER_ID")
DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")

LINE_API = "https://api.line.me/v2/bot/message/push"

app = FastAPI(title="Hear With Your Eyes API")

LAST_EVENT = {"event": None, "time": 0}
COOLDOWN = 15  # วินาที

@app.post("/api/alert")
def send_alert(data: dict):
    global LAST_EVENT

    event = data.get("event", "unknown")
    level = data.get("level", "info")
    message = data.get("message", "")
    confidence = float(data.get("confidence", 0))

    now_ts = time()

    # 🚫 กันแจ้งเตือนซ้ำ
    if LAST_EVENT["event"] == event and (now_ts - LAST_EVENT["time"]) < COOLDOWN:
        return {"status": "skipped", "reason": "duplicate in cooldown"}

    LAST_EVENT["event"] = event
    LAST_EVENT["time"] = now_ts

    # 🎨 ระดับ + emoji
    if level.lower() == "emergency":
        level_icon = "🔴"
        title = "Emergency"
        color = 0xE74C3C
    elif level.lower() == "warning":
        level_icon = "🟠"
        title = "Warning"
        color = 0xE67E22
    elif level.lower() == "caution":
        level_icon = "🟡"
        title = "Caution"
        color = 0xF1C40F
    elif level.lower() in ["general notification", "general"]:
        level_icon = "🟢"
        title = "General Notification"
        color = 0x2ECC71
    else:
        level_icon = "🔵"
        title = "Contextual Awareness"
        color = 0x3498DB

    # =========================
    # 📝 ข้อความหลัก
    # =========================
    text = (
        f"{level_icon} Hear With Your Eyes – {title}\n"
        "------------------------------\n"
        f"{message}\n"
        f"Confidence: {confidence:.1f} %\n"
        f"Time: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
    )

    # =========================
    # 📤 ส่ง LINE
    # =========================
    if LINE_TOKEN and LINE_USER_ID:
        headers = {
            "Authorization": f"Bearer {LINE_TOKEN}",
            "Content-Type": "application/json"
        }

        payload = {
            "to": LINE_USER_ID,
            "messages": [{"type": "text", "text": text}]
        }

        requests.post(LINE_API, headers=headers, json=payload)

    # =========================
    # 📤 ส่ง DISCORD
    # =========================
    if DISCORD_WEBHOOK:
        discord_payload = {
            "embeds": [
                {
                    "title": f"{level_icon} Hear With Your Eyes – {title}",
                    "description": message,
                    "color": color,
                    "fields": [
                        {"name": "Confidence", "value": f"{confidence:.1f} %", "inline": True},
                        {"name": "Time", "value": datetime.now().strftime('%d/%m/%Y %H:%M:%S'), "inline": True}
                    ]
                }
            ]
        }

        requests.post(DISCORD_WEBHOOK, json=discord_payload)

    return {"status": "ok", "channels": ["line", "discord"]}
