import os, requests, yfinance as yf
import pandas as pd

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# أسهمك
STOCKS = ["2280.SR", "4080.SR"]  # 2280=المراعي؟ عدلها انت، 4080=SIRI
NAMES = {"2280.SR": "المراعي", "4080.SR": "SIRI"}

def get_rsi(close, period=14):
    delta = close.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def analyze(symbol):
    df = yf.download(symbol, period="3mo", interval="1d", progress=False)
    if len(df) < 30: return None
    close = df['Close']
    rsi = get_rsi(close).iloc[-1]
    low_20 = df['Low'].tail(20).min()
    price = close.iloc[-1]
    change = ((price - close.iloc[-2]) / close.iloc[-2]) * 100
    
    # شروط الدخول
    if rsi < 45 and price <= low_20 * 1.05:
        target1 = price * 1.03
        target2 = price * 1.06
        stop = low_20 * 0.97
        return f"🔔 {NAMES.get(symbol, symbol)}\nالسعر: {price:.2f} ({change:+.2f}%)\nRSI: {rsi:.1f}\nقاع 20 يوم: {low_20:.2f}\n🎯 هدف1: {target1:.2f}\n🎯 هدف2: {target2:.2f}\n🛑 وقف: {stop:.2f}"
    return None

messages = []
for s in STOCKS:
    res = analyze(s)
    if res: messages.append(res)

if not messages:
    messages = ["✅ فحص اليوم: لا يوجد دخول حسب الشروط (RSI + قاع 20 يوم)"]

text = "\n\n---\n\n".join(messages)

# ارسال لتليجرام
url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
requests.post(url, data={"chat_id": CHAT_ID, "text": text})
print("تم الارسال")
