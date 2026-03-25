# Home Assistant

โฟลเดอร์นี้ใช้สำหรับเก็บไฟล์ automation ของ Home Assistant

## Files

- `automation_API.yaml`
  - ใช้สำหรับรับ event ที่ส่งมาจาก Raspberry Pi
  - เหมาะสำหรับ trigger จาก webhook / API

- `automation_HA.yaml`
  - ใช้สำหรับควบคุมอุปกรณ์ภายใน Home Assistant
  - ใช้สำหรับสร้าง notification หรือเปลี่ยนสีหลอดไฟ

## Usage

1. คัดลอกไฟล์ YAML ไปยัง Home Assistant configuration
2. โหลด automation ใหม่
3. ตรวจสอบว่า webhook URL และ entity ID ถูกต้อง

## Notes

- ควรตรวจสอบว่าชื่อ entity ของหลอดไฟใน Home Assistant ตรงกับอุปกรณ์จริง
- หากมีการใช้ notification ผ่านมือถือ ควรตั้งค่า mobile app integration ก่อน