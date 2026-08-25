import yfinance as yf
import os
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_IDS = os.getenv("CHAT_ID","").split(",")

STOCKS = [
"1120.SR","1211.SR","2222.SR","2010.SR","2280.SR","1180.SR","1150.SR","1320.SR","2380.SR","2310.SR",
"2350.SR","2030.SR","4200.SR","4165.SR","4080.SR","7010.SR","7203.SR","1810.SR","4003.SR","1010.SR",
"AAPL","MSFT","NVDA","TSLA","META","AMZN","GOOGL","NFLX","AMD","AVGO",
"PLTR","COIN","MSTR","SMCI","ARM","SHOP","SPY","QQQ","TQQQ","SOFI",
"BTC-USD","ETH-USD","SOL-USD","XRP-USD","ADA-USD","DOGE-USD","AVAX-USD","DOT-USD","LINK-USD","LTC-USD",
"BCH-USD","SHIB-USD","TRX-USD","MATIC-USD","ETC-USD","XLM-USD","ATOM-USD","HBAR-USD","PEPE-USD","BONK-USD"
]

def check(ticker):
    try:
        df = yf.download(ticker, period="1d", interval="1d", progress=False, auto_adjust=True)
        hist = yf.download(ticker, period="1mo", progress=False, auto_adjust=True)
        if len(hist) < 20: return None
        close = hist['Close']
        price = float(close.iloc[-1])
        low20 = float(close.tail(20).min())
        delta = close.diff()
        up = delta.clip(lower=0).rolling(14).mean()
        down = -delta.clip(upper=0).rolling(14).mean()
        rsi = 100 - (100/(1+up/down))
        rsi_val = float(rsi.iloc[-1])
        
        # شرط الدخول
        if rsi_val < 55 and price <= low20 * 1.06:
            # تحديد النوع
            if ".SR" in ticker:
                flag = "🇸🇦 اسهم سعودية - تاسي"
                icon = "🏢"
            elif "-USD" in ticker:
                flag = "₿ كريبتو - عملات رقمية"
                icon = "🪙"
            else:
                flag = "🇺🇸 اسهم امريكية - وول ستريت"
                icon = "🏦"
            
            t1 = price * 1.04
            t2 = price * 1.08
            stop = low20 * 0.98
            
            msg = f"🟢 فرصة دخول\n{flag}\n\n{icon} {ticker.replace('.SR','').replace('-USD','')
