import yfinance as yf, requests, os
from datetime import datetime, timezone, timedelta

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
GROUP_ID = os.getenv("GROUP_ID")

def send(text):
    # يرسل مرة وحدة بس عشان ما يكرر
    chat = GROUP_ID or CHAT_ID
    try:
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", json={"chat_id": chat, "text": text}, timeout=15)
    except: pass

try:
    data = yf.download("6013.SR", period="5d", interval="15m", progress=False)
    close = data['Close'].dropna()
    price = float(close.iloc[-1])
    
    delta = close.diff()
    gain = delta.where(delta>0,0).rolling(14).mean()
    loss = -delta.where(delta<0,0).rolling(14).mean()
    rs = gain/loss
    rsi = 100 - (100/(1+rs))
    r = float(rsi.iloc[-1])

    if r < 32: status, per = "شراء قوي 🟢", 80
    elif r < 45: status, per = "شراء 🟢", 60
    elif r > 72: status, per = "بيع قوي 🔴", 80
    elif r > 60: status, per = "بيع 🔴", 60
    else: status, per = "انتظار 🟡", 50

except Exception as e:
    price, r, status, per = 0, 50, "السوق مغلق 🌙", 0

now = datetime.now(timezone.utc) + timedelta(hours=3)
time_str = now.strftime("%I:%M %p")

msg = f"""🔥 توصيات ابو سلطان - {time_str} ⏰ كل 15 د

📊 سهم البلاد (6013.SR)
💰 السعر الحالي: {price:.2f}
📈 RSI: {r:.0f}

التوصية: {status} {per}%

🎯 دخول: {price:.2f}
🎯 هدف 1: {price*1.02:.2f} (+2%)
🛑 وقف: {price*0.98:.2f} (-2%)

⚠️ ليست نصيحة مالية"""

send(msg)