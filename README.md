# HearWithYourEyes

ระบบตรวจจับเสียงสิ่งแวดล้อมและแปลงผลลัพธ์เป็นสัญญาณแสงและการแจ้งเตือนแบบเรียลไทม์ สำหรับผู้มีปัญหาการได้ยิน เป็นระบบที่ใช้เทคโนโลยี AI + IoT 

---

## Overview

HearWithYourEyes เป็นระบบที่ช่วยให้ผู้ที่มีความบกพร่องทางการได้ยินสามารถรับรู้เหตุการณ์สำคัญผ่าน “การมองเห็น” แทนการได้ยิน

ระบบสามารถตรวจจับเสียงสำคัญได้ ตัวอย่างเช่น:

* Fire alarm / Smoke alarm
* Glass breaking
* Doorbell
* Dog bark

เมื่อระบบตรวจจับเหตุการณ์ได้ จะทำการแปลงผลลัพธ์เป็น:

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
มีไฟล์เสียงสำหรับการทดสอบระบบอยู่ใน:

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
* Raspberry Pi, Yeelight และ Home Assistant ควรอยู่ในเครือข่ายเดียวกัน
* หากมีการเปลี่ยน IP Address ของอุปกรณ์ ควรอัปเดตค่าในไฟล์ที่เกี่ยวข้อง
* ควรทดสอบไมโครโฟน หลอดไฟ และ Home Assistant ก่อนใช้งานจริง

---

## License

This project is for educational purposes only.
