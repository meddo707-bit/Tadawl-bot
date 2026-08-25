import yfinance as yf
import requests
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def calc_rsi(data, period=14):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.iloc[-1]

def get_info(symbol):
    try:
        df = yf.download(symbol, period="1mo", interval="1d", progress=False)
        if df.empty: return None
        close = float(df['Close'].iloc[-1])
        prev = float(df['Close'].iloc[-2])
        change = ((close-prev)/prev)*100
        rsi = calc_rsi(df)
        low20 = float(df['Low'].tail(20).min())
        target = close * 1.05
        stop = low20 * 0.97
        return close, change, rsi, low20, target, stop
    except:
        return None

stocks = {
    "2222.SR": "تاسي - 2222",
    "2010.SR": "تاسي - 2010",
    "2280.SR": "تاسي - 2280",
    "META": "وول ستريت - META",
    "NVDA": "وول ستريت - NVDA",
    "AAPL": "وول ستريت - AAPL",
    "BTC-USD": "كريبتو - BTC",
    "ETH-USD": "كريبتو - ETH",
    "SOL-USD": "كريبتو - SOL",
}

msg = f"توصيات ابو سلطان\n\n"

for sym, name in stocks.items():
    data = get_info(sym)
    if not data: continue
    close, change, rsi, low20, target, stop = data
    msg += f"{name}\n"
    msg += f"${close:.4f} ({change:+.2f}%)\n"
    msg += f"RSI: {rsi:.1f} | قاع 20: {low20:.4f}\n"
    msg += f"هدف: {target:.4f} (+5%) | وقف: {stop:.4f}\n\n"

msg += "---\nفحص لايف مباشر"

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
requests.post(url, data={"chat_id": CHAT_ID, "text": msg})
print(msg)
