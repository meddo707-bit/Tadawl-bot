import os, requests, time
BOT_TOKEN=os.getenv("BOT_TOKEN")
CHAT_ID=os.getenv("CHAT_ID")
def send(m):
    requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={m}", timeout=15)
send("تم ✅ البوت الجديد شغال 100%")
print("Sent!")
time.sleep(3600)
