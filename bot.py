import yfinance as yf
import time
import requests
from datetime import datetime

BOT_TOKEN = "PUT_YOUR_BOT_TOKEN_HERE"
CHAT_ID = "PUT_YOUR_CHAT_ID_HERE"

STOCKS = ["1120.SR", "1180.SR", "2010.SR", "2380.SR", "2222.SR"]

def send_telegram(msg):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": CHAT_ID, "text": msg})
    except:
        pass

def check_stock(symbol):
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period="3mo")
        if len(hist) < 20:
            return
        
        last = hist['Close'].iloc[-1]
        low_20 = hist['Low'].tail(20).min()
        high_20 = hist['High'].tail(20).max()
        
        if last <= low_20 * 1.03:
            msg = f"SUPPORT ALERT\n{symbol}\nPrice: {last:.2f}\nSupport: {low_20:.2f}\nTime: {datetime.now().strftime('%H:%M')}"
            send_telegram(msg)
        elif last >= high_20 * 0.97:
            msg = f"RESISTANCE ALERT\n{symbol}\nPrice: {last:.2f}\nResistance: {high_20:.2f}\nTime: {datetime.now().strftime('%H:%M')}"
            send_telegram(msg)
            
    except Exception as e:
        print(f"Error {symbol}: {e}")

print("Bot started...")
send_telegram("Bot started successfully")

while True:
    for sym in STOCKS:
        check_stock(sym)
        time.sleep(2)
    time.sleep(300)
