import yfinance as yf
import os
import requests
import traceback

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

def get_signal(t):
    try:
        df = yf.download(t, period="1mo", progress=False, auto_adjust=True)
        if df.empty or len(df) < 21:
            return None
        close = df['Close']
        price = float(close.iloc[-1])
        low20 = float(close.tail(20).min())
        # RSI
        d = close.diff()
        g = d.where(d>0,0).rolling(14).mean()
        l = -d.where(d<0,0).rolling(14).mean()
        rsi = 100 - (100/(1+g/l))
        r = float(rsi.iloc[-1])

        if r < 55 and price <= low20*1.06:
            if ".SR" in t:
                head = "🟢 فرصة دخول\n🇸🇦 اسهم سعودية - تاسي"
                icon = "🏢"
            elif "-USD" in t:
                head = "🟢 فرصة دخول\n₿ كريبتو - عملات رقمية"
                icon = "🪙"
            else:
                head = "🟢 فرصة دخول\n🇺🇸 اسهم امريكية - وول ستريت"
                icon = "🏦"
            
            name = t.replace(".SR","").replace("-USD","")
            return f"{head}\n\n{icon} {name}\n💰 السعر: {price:.4f}\n📊 RSI: {r:.1f}\n📉 قاع 20 يوم: {low20:.4f}\n\n🎯 هدف 1: {price*1.04:.4f} (+4%)\n🎯 هدف 2: {price*1.08:.4f} (+8%)\n🔴 وقف: {low20*0.98:.4f}"
    except Exception as e:
        print(f"Error {t}: {e}")
        return None
    return None

msgs=[]
for s in STOCKS:
    sig = get_signal(s)
    if sig:
        msgs.append(sig)

if not msgs:
    text = "✅ اليوم شغال - فحص الساعة\nلا يوجد فرص حسب الشروط الحالية\n📊 فحص 60 سهم (20 سعودي + 20 امريكي + 20 كريبتو ₿)"
else:
    text = "🔥 توصيات ابو سلطان 🔥\n\n" + "\n\n---\n\n".join(msgs)

for cid in CHAT_IDS:
    cid=cid.strip()
    if cid:
        try:
            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data={"chat_id":cid,"text":text}, timeout=20)
        except:
            pass
