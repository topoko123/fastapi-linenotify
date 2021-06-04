# fastapi-linenotify

#### ขั้นตอนมีดังนี้
                
+ เข้าไปที่ https://notify-bot.line.me/my/services/
    + ทำการลงทะเบียนบริการ
    + กรอกข้อมูลให้ครบ
    + นำ Client Id กับ Secret มาใส่ในโค้ด
    + อ่านเพิ่มเติมได้ที่ https://notify-bot.line.me/doc/en/
+ สร้าง Project
    + อ่านเพิ่มเติมเกี่ยวกับ FastAPI: https://fastapi.tiangolo.com/
+ สร้างหน้าฟอร์ม
    * ทำ button สำหรับ request ไปยัง API
    
    
#### Package ที่ต้องติดตั้ง
```sh
$ pip install fastapi
$ pip install uvicorn[standard]
$ pip install requests
$ pip install python-multipart
```

#### สำหรับ Clone repo
```sh
$ python -m pip install -r requirements.txt
```
### สามารถนำไปประยุกต์ใช้งานได้ เข่น เมื่อได้รับ access_token จากผู้ใช้งาน ก็ทำการจัดเก็บลงฐานข้อมูล เมื่อเราต้องการส่งข้อความก็สามารถส่งข้อความไปหาผู้ใช้ตาม access_token ที่เราจัดเก็บไว้ในฐานข้อมูลได้
