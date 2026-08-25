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

def check_stock(ticker):
    try:
        data = yf.download(ticker, period="1mo", progress=False)
        if len(data) < 20:
            return None
        close = data['Close']
        price = float(close.iloc[-1])
        low20 = float(close.tail(20).min())
        # RSI بسيط
        delta = close.diff()
        up = delta.clip(lower=0).rolling(14).mean()
        down = -delta.clip(upper=0).rolling(14).mean()
        rsi = 100 - (100 / (1 + up/down))
        rsi_val = float(rsi.iloc[-1])
        if rsi_val < 52 and price <= low20 * 1.05:
            return f"✅ {ticker} | {price:.2f} | RSI {rsi_val:.1f}"
    except:
        return None
    return None

found = []
for t in STOCKS:
    r = check_stock(t)
    if r:
        found.append(r)

if not found:
    text = "📊 فحص 60 سهم (20 سعودي + 20 امريكي + 20 كريبتو)\nلا يوجد فرص RSI<52 حاليا - السوق مرتفع"
else:
    text = "🔥 توصيات ابو سلطان - 60 سهم 🔥\n\n" + "\n".join(found) + "\n\n⚠️ ليست نصيحة مالية"

for cid in CHAT_IDS:
    cid = cid.strip()
    if cid:
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data={"chat_id":cid,"text":text})
