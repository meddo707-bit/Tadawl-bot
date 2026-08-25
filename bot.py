import yfinance as yf
import pandas as pd
import os
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_IDS = os.getenv("CHAT_ID", "").split(",")

# 60 سهم
STOCKS = [
    # 20 سعودي
    "1120.SR","1211.SR","2222.SR","2010.SR","2280.SR","1180.SR","1150.SR","1320.SR","2380.SR","2310.SR",
    "2350.SR","2030.SR","4200.SR","4165.SR","4080.SR","7010.SR","7203.SR","1810.SR","4003.SR","1010.SR",
    # 20 امريكي
    "AAPL","MSFT","NVDA","TSLA","META","AMZN","GOOGL","NFLX","AMD","AVGO",
    "PLTR","COIN","MSTR","SMCI","ARM","SHOP","SPY","QQQ","TQQQ","SOFI",
    # 20 كريبتو
    "BTC-USD","ETH-USD","SOL-USD","XRP-USD","ADA-USD","DOGE-USD","AVAX-USD","DOT-USD","LINK-USD","LTC-USD",
    "BCH-USD","SHIB-USD","TRX-USD","MATIC-USD","ETC-USD","XLM-USD","ATOM-USD","HBAR-USD","PEPE-USD","BONK-USD"
]

def get_rsi(prices, period=14):
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def check_stock(ticker):
    try:
        df = yf.download(ticker, period="1mo", interval="1d", progress=False)
        if len(df) < 21: return None
        close = df['Close']
        if isinstance(close, pd.DataFrame): close = close.iloc[:,0]
        rsi = get_rsi(close).iloc[-1]
        price = float(close.iloc[-1])
        low_20 = float(close.tail(20).min())
        # شرط خفيف عشان تجيك توصيات يوميا
        if rsi < 50 and price <= low_20 * 1.03:
            return f"✅ {ticker} | سعر {price:.2f} | RSI {rsi:.1f} | قريب من قاع 20 يوم {low_20:.2f} | هدف +3% و +5%"
    except: return None
    return None

def main():
    picks = []
    for t in STOCKS:
        r = check_stock(t)
        if r: picks.append(r)
    
    if not picks:
        msg = "📊
