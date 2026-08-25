import os, requests, yfinance as yf
import pandas as pd

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_IDS = [c.strip() for c in os.getenv("CHAT_ID","").split(",") if c.strip()]

STOCKS = ["2280.SR", "4080.SR"]
NAMES = {"2280.SR": "المراعي", "4080.SR": "STC"}

def get_rsi(close, period=14):
    delta = close.diff()
    gain = (delta.where(delta > 0, 0)).rolling(period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def analyze(symbol):
    df = yf.download(symbol, period="3mo", interval="1d", progress=False)
    if len(df) < 30:
        return None

    # اصلاح مشكلة السيريز
    close = df['Close']
    if isinstance(close, pd.DataFrame):
        close = close.iloc[:, 0]
    close = close.dropna()

    low = df['Low']
    if isinstance(low, pd.DataFrame):
        low = low.iloc[:, 0]

    rsi_series = get_rsi(close)

    # نحول كل شي لرقم واحد فقط
    rsi = float(rsi_series.iloc[-1])
    price = float(close.iloc[-1])
    prev = float(close.iloc[-2])
    low_20 = float(low.tail(20).min())

    change = ((price - prev) / prev) * 100

    # شرط الدخول - العين كلها ارقام مو Series
    if rsi < 45 and price <= low_20 * 1.05:
        target1 = price * 1.03
        target2 = price * 1.06
        stop = low_20 * 0.97
        return f"🔔 {NAMES.get(symbol, symbol)} ({symbol})\nالسعر: {price:.2f} ({change:+.2f}%)\nRSI: {rsi:.1f}\nالدخول: {price:.2f}\nهدف1: {target1:.2f}\nهدف2: {target2:.2f}\nوقف: {stop:.2f}"

    return None

messages = []
for s in STOCKS:
    try:
        res = analyze(s)
        if res:
            messages.append(res)
    except Exception as e:
        print(f"خطأ في {s}: {e}")

if not messages:
    messages = ["✅ اليوم شغال - فحص الساعة - لا يوجد فرص حسب الشروط الحالية"]

text = "\n\n---\n\n".join(messages)

# الارسال للقروب والخاص مع بعض
for CHAT_ID in CHAT_IDS:
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    r = requests.post(url, data={"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"})
    print(f"Sent to {CHAT_ID}: {r.text}")
