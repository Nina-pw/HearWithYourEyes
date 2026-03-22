# HearWithYourEyes

ระบบตรวจจับเสียงสิ่งแวดล้อมและแปลงผลลัพธ์เป็นสัญญาณแสงและการแจ้งเตือนแบบเรียลไทม์ สำหรับผู้มีปัญหาการได้ยิน

---

## Requirements

### Hardware

* Raspberry Pi 4
* Microphone (ReSpeaker 2-Mic HAT)
* Smart Bulb (Yeelight)
* Smartphone

### Software

* Python 3.9+
* TensorFlow Lite
* Home Assistant

---

## Project Structure

```bash
src/                # source code
config/             # configuration ของระบบ
homeassistant/      # automation สำหรับ Home Assistant
models/             # AI model (yamnet.tflite)
data/               # dataset และ evaluation data
evaluation/         # ประเมินและผลลัพธ์ของระบบ (xlsx)
```

---

## Dataset

โครงงานนี้ใช้ชุดข้อมูล **UrbanSound8K**

Download:
https://urbansounddataset.weebly.com/urbansound8k.html

หลังจากดาวน์โหลด ให้วางไว้ที่:

```bash
data/urbansound8k/
```

หมายเหตุ:
มีตัวอย่างไฟล์เสียงสำหรับทดสอบอยู่ใน:

```bash
data/evaluationSound/
```

---

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/your-username/HearWithYourEyes.git
cd HearWithYourEyes
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Prepare Dataset

* ดาวน์โหลด UrbanSound8K
* แตกไฟล์ไว้ในโฟลเดอร์ `data/`

---

## Configuration

### Microphone

ตรวจสอบอุปกรณ์:

```bash
arecord -l
```

---

### Smart Light (Yeelight)

* เปิด LAN Control ในแอป
* ใส่ IP ในไฟล์ config

---

### Home Assistant

* ตั้งค่า Webhook / REST API
* เพิ่ม Automation สำหรับแจ้งเตือน

---

## ▶Usage

รันระบบ:

```bash
python main.py
```

---

## Testing

```bash
python test/test_inference.py
```

---

## License

This project is developed for educational purposes.
