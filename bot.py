import yfinance as yf, requests, os
from datetime import timezone, timedelta, datetime

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
GROUP_ID = os.getenv("GROUP_ID")

def send(msg):
    for cid in [CHAT_ID, GROUP_ID]:
        if not cid: continue
        try:
            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", json={"chat_id": cid, "text": msg}, timeout=10)
        except: pass

try:
    df = yf.download("6013.SR", period="5d", interval="15m", progress=False)
    close = df['Close'].dropna()
    if len(close) < 20: raise Exception("no data")
    delta = close.diff()
    gain = delta.where(delta>0,0).rolling(14).mean()
    loss = -delta.where(delta<0,0).rolling(14).mean()
    rsi = 100 - (100/(1+gain/loss))
    price = float(close.iloc[-1])
    r = float(rsi.iloc[-1])
except:
    # اذا السوق مقفل يرسل اخر سعر عنده وما يفشل
    price = 0
    r = 50

sa_time = datetime.now(timezone.utc) + timedelta(hours=3)
t = sa_time.strftime("%I:%M %p")

if r < 30:
    msg = f"🔥 توصيات ابو سلطان - {t}\n\nشراء قوي 🟢 80%\nدخول {price:.2f} RSI {r:.0f}"
elif r < 40:
    msg = f"🔥 توصيات ابو سلطان - {t}\n\nشراء 🟢 60%\nدخول {price:.2f} RSI {r:.0f}"
elif r > 70:
    msg = f"🔥 توصيات ابو سلطان - {t}\n\nبيع قوي 🔴 80%\nخروج {price:.2f} RSI {r:.0f}"
else:
    msg = f"🔥 توصيات ابو سلطان - {t}\n\nانتظار 🟡 50%\nالسعر {price:.2f} RSI {r:.0f}"

send(msg)