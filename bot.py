import yfinance as yf
import time, requests, os

BOT_TOKEN=os.getenv("BOT_TOKEN")
CHAT_ID=os.getenv("CHAT_ID")

# قائمة مدمجة - سعودي + امريكي رخيص مضاربي
STOCKS=[
    # سعودي
    "1120.SR","2222.SR","7010.SR","1180.SR","2010.SR",
    # امريكي رخيص مضاربة
    "SOFI","NIO","MARA","RIOT","F","SNAP","LCID","HOOD","BB","PLTR"
]

def send(m):
    try:
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",json={"chat_id":CHAT_ID,"text":m})
    except:
        pass

def check(s):
    try:
        h=yf.Ticker(s).history(period="6mo")
        if len(h)<30: return None
        last=float(h['Close'].iloc[-1])
        low=float(h['Low'].tail(20).min())
        high=float(h['High'].tail(20).max())
        change = ((last - h['Close'].iloc[-2])/h['Close'].iloc[-2])*100
        
        d=h['Close'].diff()
        g=d.where(d>0,0).rolling(14).mean()
        l=-d.where(d<0,0).rolling(14).mean()
        rsi=100-(100/(1+g/l))
        r=float(rsi.iloc[-1])
        
        av=h['Volume'].tail(20).mean()
        lv=h['Volume'].iloc[-1]
        vol_ratio = lv/av if av>0 else 1

        is_saudi = ".SR" in s
        market = "🇸🇦 تاسي - السعودي" if is_saudi else "🇺🇸 وول ستريت - الامريكي"
        currency = "ريال" if is_saudi else "$"

        # شرط الدخول
        if last<=low*1.02 and r<40 and lv>av*0.8:
            return f"""🟢 توصية مضاربية قوية
{market}
━━━━━━━━━━━━
🏢 السهم: {s}
💰 السعر: {last:.2f} {currency} ({change:+.2f}%)

📊 RSI(14): {r:.1f} - تشبع بيعي
📦 السيولة: {vol_ratio:.1f}x
📉 قاع 20 يوم: {low:.2f}

🎯 هدف 1: {last*1.04:.2f} (+4%)
🎯 هدف 2: {last*1.08:.2f} (+8%)
🛑 وقف: {last*0.97:.2f} (-3%)
⏰ مضاربة 3-7 ايام
"""
    except Exception as e:
        print(e)
        return None

send("✅ البوت المدمج V4 اشتغل\n🇸🇦 5 اسهم سعودية + 🇺🇸 10 اسهم امريكية رخيصة")
while True:
    for s in STOCKS:
        m=check(s)
        if m:
            send(m)
        time.sleep(3)
    time.sleep(300)
