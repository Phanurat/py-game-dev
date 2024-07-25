import requests
import time
import hashlib
import hmac

# ข้อมูลที่ได้รับจาก Shopee
partner_id = 'your_partner_id'
shop_id = 'your_shop_id'
partner_key = 'your_partner_key'
access_token = 'your_access_token'

# ตั้งค่าเวลา timestamp
timestamp = int(time.time())

# สร้างข้อความที่จะใช้ในการสร้างลายเซ็น
base_string = f"{partner_id}{access_token}{timestamp}"
sign = hmac.new(partner_key.encode(), base_string.encode(), hashlib.sha256).hexdigest()

# ตั้งค่า URL
url = f"https://partner.shopeemobile.com/api/v2/product/get_category?access_token={access_token}&language=zh-hans&partner_id={partner_id}&shop_id={shop_id}&sign={sign}&timestamp={timestamp}"

# ส่ง request
response = requests.get(url)

# แสดงผลลัพธ์
print(response.text)
