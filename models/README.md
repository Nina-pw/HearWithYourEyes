# Models

โฟลเดอร์นี้ใช้สำหรับเก็บโมเดล AI และไฟล์ label map

## Required Files

- `yamnet.tflite`
- `yamnet_class_map.csv`

ไฟล์เหล่านี้ควรวางไว้ใน:

```bash
models/
```

## Source

โมเดล YAMNet สามารถดูข้อมูลเพิ่มเติมได้จาก:
https://tfhub.dev/google/yamnet/1

## Notes

- หากไม่มีไฟล์เหล่านี้ ระบบจะไม่สามารถทำงานได้
- ตรวจสอบให้แน่ใจว่า path ใน `raspberry_pi.py` ตรงกับตำแหน่งไฟล์จริง