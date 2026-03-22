# HearWithYourEyes

ระบบตรวจจับเสียงสิ่งแวดล้อมและแปลงผลลัพธ์เป็นสัญญาณแสงและการแจ้งเตือนแบบเรียลไทม์ สำหรับผู้มีปัญหาการได้ยิน

---

## Requirements

### Hardware

* Raspberry Pi 4
* Microphone (ReSpeaker 2-Mic HAT)
* Smart Bulb (Yeelight W3 Multicolor)
* Smartphone Notification (Line & Discord)

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
evaluation/         # ประเมินและผลลัพธ์ของระบบ (test results)
```

---

## Dataset

ใช้ชุดข้อมูล **UrbanSound8K**

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

## Installation & Build

### 1. Clone Repository

```bash
git clone https://github.com/your-username/HearWithYourEyes.git
cd HearWithYourEyes
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

## 3. Setup Model

ดาวน์โหลดไฟล์:

* yamnet.tflite
* yamnet_class_map.csv

แล้ววางใน:

```
models/
```

## 4. Setup Dataset

ดาวน์โหลด UrbanSound8K และวางไว้ใน:

```
data/urbansound8k/
```

---

## Configuration

## 1. Microphone (Raspberry Pi)

ตรวจสอบอุปกรณ์:

```bash
arecord -l
```

ทดสอบบันทึกเสียง:

```bash
arecord -D plughw:1,0 test.wav
```

## 2. Smart Light (Yeelight W3 Multicolor)

* เปิด **LAN Control** ในแอป Yeelight
* หา IP ของหลอดไฟ

แก้ไขไฟล์ config:

```yaml
light_ip: "192.168.x.x"
```

## 3. Home Assistant

### วิธีเชื่อมต่อ:

* ใช้ **REST API / Webhook**

ตัวอย่าง config:

```yaml
webhook_url: "http://homeassistant.local:8123/api/webhook/sound_event"
```

### ตั้งค่า Automation:

* รับ event จาก Raspberry Pi
* สั่งเปิดไฟ / แจ้งเตือนมือถือ

---

## Usage

รันระบบบน Raspberry Pi:

```bash
python src/raspberry_pi/raspberry_pi.py
```

---

## Testing

```bash
python test/test_inference.py
```

---

## License

This project is for educational purposes only.
