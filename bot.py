import os
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

msg = f"✅ البوت اشتغل تمام!\nID حقك: {CHAT_ID}\nجاهز للتداول"

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
r = requests.post(url, data={"chat_id": CHAT_ID, "text": msg})
print(r.text)
