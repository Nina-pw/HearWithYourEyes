# Source Code

โฟลเดอร์นี้ใช้สำหรับเก็บ source code หลักของระบบ

## Structure

- `api/`
  - โค้ดที่เกี่ยวข้องกับ notification หรือ API integration

- `audio/`
  - โค้ดที่เกี่ยวข้องกับ audio preprocessing

- `raspberry_pi/`
  - โค้ดหลักที่ใช้รันระบบบน Raspberry Pi

## Notes

- ควรอ่านค่าการตั้งค่าจาก config file แทนการ hardcode ค่าในโค้ด
- หากมีการแก้ไข path ของโมเดลหรือ endpoint ต่าง ๆ ควรตรวจสอบให้ตรงกับไฟล์ config