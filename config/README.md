# Config

โฟลเดอร์นี้ใช้สำหรับเก็บไฟล์กำหนดค่าของระบบ โดยแบ่งออกเป็น 2 ส่วนหลัก

## Files

### `app_config.yaml`
ใช้สำหรับกำหนดค่าของโปรแกรมฝั่ง Raspberry Pi / Python เช่น:
- model path
- class map path
- Home Assistant webhook URL
- Yeelight IP
- microphone settings
- threshold และ cooldown

### `configuration.yaml`
ใช้สำหรับกำหนดค่าของ Home Assistant เช่น:
- frontend
- automation / script / scene
- REST command สำหรับ LINE notification
- REST command สำหรับ API ภายในระบบ

## Notes

- `app_config.yaml` ถูกอ่านโดย Python script
- `configuration.yaml` ถูกใช้งานโดย Home Assistant
- ไม่ควรใส่ secret จริง เช่น access token หรือ user ID ลงใน public repository