import yfinance as yf
import os
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_IDS = os.getenv("CHAT_ID", "").split(",")

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
        df = yf.download(ticker, period="1mo", progress=False, auto_adjust=True)
        if len(df) < 20:
            return None
        close = df['Close'].iloc[:,0] if hasattr(df['Close'], 'iloc') and len(df['Close'].shape)>1 else df['Close']
        price = float(close.iloc[-1])
        low20 = float(close.tail(20).min())
        # RSI مبسط
        delta = close.diff()
        gain = delta.where(delta>0,0).rolling(14).mean().iloc[-1]
        loss = -delta.where(delta<0,0).rolling(14).mean().iloc[-1]
        rs = gain / loss if loss != 0 else 0
        rsi = 100 - (100/(1+rs)) if loss !=0 else 50
        
        if rsi < 50 and price <= low20*
