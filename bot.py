import yfinance as yf
import time
import requests
import os
from datetime import datetime

BOT_TOKEN = os.getenv("BOT_TOKEN", "PUT_YOUR_BOT_TOKEN_HERE")
CHAT_ID = os.getenv("CHAT_ID", "PUT_YOUR_CHAT_ID_HERE")

STOCKS = ["1120.SR", "2222.SR", "7010.SR", "1180.SR", "2010.SR", "2380.SR", "2200.SR", "6015.SR", "2082.SR", "7203.SR", "1211.SR", "2280.SR", "1150.SR", "1080.SR", "1060.SR", "1010.SR", "2030.SR", "2223.SR", "4165.SR", "7202.SR"]

def send_telegram(msg):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})
    except:
        pass

def check_stock(symbol):
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period="3mo")
        if len(hist) < 20:
            return None
        last = hist['Close'].iloc[-1]
        low_20 = hist['Low'].tail(20).min()
        high_20 = hist['High'].tail(20).max()
        if last <= low_20 * 1.02:
            return f"BUY {symbol} Price {last:.2f} Low {low_20:.2f} Target {last*1.04:.2f} Stop {low_20*0.98:.2f}"
        if last >= high_20 * 0.98:
            return f"SELL {symbol} Price {last:.2f} High {high_20:.2f} Take Profit"
    except:
        pass
    return None

send_telegram(f"BOT STARTED Watching {len(STOCKS)} stocks")

while True:
    for s in STOCKS:
        msg = check_stock(s)
        if msg:
            send_telegram(msg)
        time.sleep(5)
    time.sleep(300)
