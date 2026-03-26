# HearWithYourEyes

ระบบตรวจจับเสียงสิ่งแวดล้อมและแปลงผลลัพธ์เป็นสัญญาณแสงและการแจ้งเตือนแบบเรียลไทม์ สำหรับผู้มีความบกพร่องทางการได้ยิน โดยใช้เทคโนโลยี AI และ IoT

---

## Overview

HearWithYourEyes เป็นระบบที่ช่วยให้ผู้ใช้งานสามารถรับรู้เหตุการณ์สำคัญผ่าน “การมองเห็น” แทนการได้ยิน โดยตรวจจับเสียงจากสิ่งแวดล้อมและแปลงเป็นการแจ้งเตือนในรูปแบบต่าง ๆ

ระบบสามารถตรวจจับเสียงสำคัญได้ ตัวอย่างเช่น:

* Fire alarm / Smoke alarm
* Glass breaking
* Doorbell
* Dog bark

เมื่อระบบตรวจจับเหตุการณ์ได้ จะทำการแสดงผลผ่าน:

* การแสดงผลด้วยสีของแสง (Smart Light)
* การแจ้งเตือนผ่านสมาร์ตโฟน (LINE / Discord)

---

## System Concept

* Raspberry Pi รับเสียงจาก Microphone
* ใช้โมเดล **YAMNet (TensorFlow Lite)** จำแนกเสียง
* ประเมินระดับความสำคัญของเหตุการณ์ (Emergency / Warning / General / Context)
* ส่งข้อมูลไปยัง Home Assistant
* ควบคุม Smart Light (Yeelight)
* ส่งแจ้งเตือนไปยังสมาร์ตโฟนของผู้ใช้แบบเรียลไทม์

---

## Quick Start

1. Clone repository
2. Install dependencies
3. ตั้งค่า `config/app_config.yaml`
4. ตรวจสอบไมโครโฟนบน Raspberry Pi
5. ตั้งค่า Home Assistant และ Yeelight
6. รันระบบด้วยคำสั่ง `python src/raspberry_pi/raspberry_pi.py --mic --loop`

---

## Project Structure

```bash
src/
├── api/              # notification / API integration
├── audio/            # audio preprocessing
└── raspberry_pi/     # main runtime for Raspberry Pi

config/               # configuration files
homeassistant/        # automation YAML สำหรับ Home Assistant
models/               # AI model and label map (yamnet.tflite)
data/
└── evaluationSound/  # evaluation audio files
evaluation/           # ประเมินและผลลัพธ์ของระบบ evaluation results (xlsx)
```

---

## Dataset

โครงงานนี้ใช้ชุดข้อมูล **UrbanSound8K** สำหรับการพัฒนาและอ้างอิงคลาสเสียงบางส่วน

Download:
https://urbansounddataset.weebly.com/urbansound8k.html

หลังจากดาวน์โหลด ให้วางไว้ที่:

```bash
data/urbansound8k/
```

หมายเหตุ:
มีไฟล์เสียงสำหรับการทดสอบระบบอยู่ใน

```bash
data/evaluationSound/
```

---

## Requirements

### Hardware

* Raspberry Pi 4
* Microphone (ReSpeaker 2-Mic HAT)
* Smart Bulb (Yeelight W3 Multicolor)
* Smartphone (LINE / Discord Notification)

### Software

* Python 3.9+
* TensorFlow Lite
* Home Assistant

---

# Installation & Build

## 1. Clone Repository

```bash
git clone https://github.com/Nina-pw/HearWithYourEyes.git
cd HearWithYourEyes
```

## 2. Install Python Dependencies

ติดตั้งไลบรารีที่จำเป็นด้วยคำสั่ง:

```bash
pip install -r requirements.txt
```

หมายเหตุ: 
หาก Raspberry Pi ใช้เวอร์ชัน Python หรือ OS ที่ต่างออกไป อาจต้องติดตั้ง `tflite-runtime` ให้ตรงกับสภาพแวดล้อมของเครื่อง

## 3. Setup Model

เตรียมไฟล์ต่อไปนี้:

```bash
yamnet.tflite
yamnet_class_map.csv
```

จากนั้นวางไฟล์ไว้ใน:

```bash
models/
```

## 4. Setup Dataset

ดาวน์โหลด **UrbanSound8K** และวางไว้ใน:

```bash
data/urbansound8k/
```

---

# Configuration

ก่อนเริ่มใช้งานระบบ ควรตรวจสอบและกำหนดค่าต่าง ๆ ให้สอดคล้องกับอุปกรณ์ เครือข่าย และบริการที่ใช้งาน เพื่อให้ Raspberry Pi, Yeelight และ Home Assistant สามารถเชื่อมต่อกันได้อย่างถูกต้อง

---

## 1. Files to Configure

ไฟล์หลักที่เกี่ยวข้องกับการกำหนดค่าระบบ มีดังนี้:

### `config/app_config.yaml`

ใช้สำหรับกำหนดค่าหลักของโปรแกรมฝั่ง Raspberry Pi / Python เช่น:

* path ของโมเดลและ class map
* Home Assistant webhook URL
* IP Address ของ Yeelight
* microphone settings
* threshold และ cooldown

### `config/configuration.yaml`

ใช้สำหรับกำหนดค่าในฝั่ง Home Assistant เช่น:

* REST command สำหรับส่งข้อความผ่าน LINE
* REST command สำหรับส่งข้อมูล alert ภายในระบบ
* การตั้งค่า automation / script / scene

### `homeassistant/automation_API.yaml`

ใช้สำหรับรับ event ที่ส่งมาจาก Raspberry Pi

### `homeassistant/automation_HA.yaml`

ใช้สำหรับกำหนดการแจ้งเตือนและการควบคุมอุปกรณ์ภายใน Home Assistant

---

## 2. Microphone (Raspberry Pi)

ตรวจสอบว่า Raspberry Pi ตรวจพบไมโครโฟนแล้ว:

```bash
arecord -l
```

ทดสอบบันทึกเสียง:

```bash
arecord -D plughw:1,0 test.wav
```

หากสามารถบันทึกเสียงได้ แสดงว่าไมโครโฟนพร้อมใช้งาน

หมายเหตุ:
หากหมายเลขอุปกรณ์ (device index) ไม่ใช่ 1,0 ให้ปรับตามผลลัพธ์ที่ได้จาก `arecord -l`

## 3. Smart Light (Yeelight W3 Multicolor)

เพื่อให้ระบบสามารถควบคุมหลอดไฟ Yeelight ได้:

1. เชื่อมต่อหลอดไฟกับ Wi-Fi เดียวกับ Raspberry Pi
2. เปิดใช้งาน **LAN Control** ในแอป Yeelight
3. ตรวจสอบ IP Address ของหลอดไฟ
4. นำค่า IP ไปกำหนดใน `config/app_config.yaml`

ตัวอย่าง:

```yaml
yeelight_ip: "192.168.x.x"
```

## 4. Home Assistant Integration

ระบบเชื่อมต่อกับ Home Assistant ผ่าน **Webhook** และ **REST Command**

Home Assistant สามารถนำข้อมูลนี้ไปใช้สำหรับ:

* เปลี่ยนสีของ Smart Light
* ส่งการแจ้งเตือน
* เรียกใช้งาน automation อื่น ๆ ภายในระบบ

---

# Usage

รันระบบบน Raspberry Pi:

```bash
python src/raspberry_pi/raspberry_pi.py --mic --loop
```

หรือรันแบบครั้งเดียว:

```bash
python src/raspberry_pi/raspberry_pi.py --mic
```

---

## Run Notification API

```bash
uvicorn src.api.api_noti:app --host 0.0.0.0 --port 8000
```

ใช้สำหรับรับข้อมูลเหตุการณ์และส่งแจ้งเตือนไปยัง LINE และ Discord

---

## Run Automatically on Startup

หากต้องการให้ระบบเริ่มทำงานอัตโนมัติเมื่อ Raspberry Pi เปิดเครื่อง สามารถตั้งค่าเป็น `systemd service` ได้

### 1. Create service file

```bash
sudo nano /etc/systemd/system/hear.service
```

### 2. Add the following configuration

```ini
[Unit]
Description=Hear With Your Eyes Service
After=network.target

[Service]
User=pi
WorkingDirectory=/home/pi/HearWithYourEyes
ExecStart=/usr/bin/python3 /home/pi/HearWithYourEyes/src/raspberry_pi/raspberry_pi.py --mic --loop
Restart=always

[Install]
WantedBy=multi-user.target
```

### 3. Enable and start the service

```bash
sudo systemctl daemon-reload
sudo systemctl enable hear.service
sudo systemctl start hear.service
```

### 4. Check service status

```bash
sudo systemctl status hear.service
```

หมายเหตุ:

* ควรตรวจสอบ path ของโปรเจกต์ให้ตรงกับตำแหน่งจริงบน Raspberry Pi
* หากมีการใช้ Virtual Environment ควรแก้ `ExecStart` ให้ตรงกับ Python interpreter ที่ใช้งาน

---

## Evaluation

สามารถใช้ไฟล์เสียงใน:

```bash
data/evaluationSound/
```

สำหรับทดสอบการทำงานของระบบ และบันทึกผลลัพธ์ไว้ใน:

```bash
evaluation/
```

---

## Notes

* Dataset UrbanSound8K มีขนาดใหญ่ จึงไม่รวมอยู่ใน Git repository
* อุปกรณ์ทั้งหมดควรอยู่ในเครือข่ายเดียวกัน
* หากมีการเปลี่ยน IP Address ของอุปกรณ์ ควรอัปเดตค่าในไฟล์ที่เกี่ยวข้อง
* ควรทดสอบไมโครโฟน หลอดไฟ และ Home Assistant ก่อนใช้งานจริง
* สภาพแวดล้อมที่มีเสียงรบกวนสูงอาจส่งผลต่อความแม่นยำ

---

## License

This project is for educational purposes only.
