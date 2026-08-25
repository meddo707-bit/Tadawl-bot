import yfinance as yf
import time, requests, os

BOT_TOKEN=os.getenv("BOT_TOKEN")
CHAT_ID=os.getenv("CHAT_ID")

STOCKS=[
    # 🇸🇦 20 سهم سعودي - نفس الاولى
    "1120.SR","2222.SR","7010.SR","1180.SR","2010.SR",
    "1150.SR","1211.SR","2380.SR","2030.SR","2020.SR",
    "1080.SR","1060.SR","1030.SR","1050.SR","1140.SR",
    "1210.SR","2350.SR","2280.SR","2180.SR","2080.SR",
    
    # 🇺🇸 20 سهم امريكي رخيص مضاربة
    "SOFI","NIO","MARA","RIOT","F","SNAP","LCID","HOOD","BB","PLTR",
    "PLUG","CHPT","NOK","SIRI","T","INTC","PFE","AMC","GME","SNDL",
    
    # ₿ 20 عملة رقمية
    "BTC-USD","ETH-USD","SOL-USD","XRP-USD","ADA-USD",
    "DOGE-USD","SHIB-USD","AVAX-USD","DOT-USD","MATIC-USD",
    "LINK-USD","LTC-USD","UNI-USD","PEPE-USD","BONK-USD",
    "FLOKI-USD","WIF-USD","TRX-USD","BNB-USD","ARB-USD"
]

def send(m):
    try:
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",json={"chat_id":CHAT_ID,"text":m})
    except: pass

def check(s):
    try:
        h=yf.Ticker(s).history(period="6mo")
        if len(h)<30: return None
        last=float(h['Close'].iloc[-1])
        low=float(h['Low'].tail(20).min())
        change=((last-h['Close'].iloc[-2])/h['Close'].iloc[-2])*100
        
        d=h['Close'].diff()
        g=d.where(d>0,0).rolling(14).mean()
        l=-d.where(d<0,0).rolling(14).mean()
        rsi=100-(100/(1+g/l))
        r=float(rsi.iloc[-1])
        
        av=h['Volume'].tail(20).mean()
        lv=h['Volume'].iloc[-1]

        # تحديد السوق
        if ".SR" in s:
            market = "🇸🇦 اسهم سعودية - تاسي"
            cur = "ريال"
        elif "-USD" in s:
            market = "₿ عملات رقمية - كريبتو"
            cur = "$"
        else:
            market = "🇺🇸 اسهم امريكية - وول ستريت"
            cur = "$"

        if last<=low*1.02 and r<40 and lv>av*0.7:
            return f"""🟢 فرصة دخول
{market}
━━━━━━━━━━━━
🏢 {s}
💰 السعر: {last:.4f} {cur} ({change:+.2f}%)
📊 RSI: {r:.1f}
📉 قاع 20 يوم: {low:.4f}

🎯 هدف 1: {last*1.04:.4f} (+4%)
🎯 هدف 2: {last*1.08:.4f} (+8%)
🛑 وقف: {last*0.97:.4f}
"""
    except: return None

send("✅ البوت الوحش V5 اشتغل\n🇸🇦 20 سعودي + 🇺🇸 20 امريكي + ₿ 20 عملة")
while True:
    for s in STOCKS:
        m=check(s)
        if m: send(m)
        time.sleep(2)
    time.sleep(300)
