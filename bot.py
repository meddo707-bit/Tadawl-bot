import yfinance as yf
import time, requests, os

BOT_TOKEN=os.getenv("BOT_TOKEN")
CHAT_ID=os.getenv("CHAT_ID")
STOCKS=["1120.SR","2222.SR","7010.SR","1180.SR","2010.SR","2380.SR","2200.SR","6015.SR","2082.SR","1150.SR"]

def send(m):
    try:
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",json={"chat_id":CHAT_ID,"text":m})
    except:
        pass

def check(s):
    try:
        h=yf.Ticker(s).history(period="6mo")
        if len(h)<30:
            return None
        last=float(h['Close'].iloc[-1])
        low=float(h['Low'].tail(20).min())
        high=float(h['High'].tail(20).max())
        open_p=float(h['Open'].iloc[-1])
        change = ((last - h['Close'].iloc[-2])/h['Close'].iloc[-2])*100
        
        d=h['Close'].diff()
        g=d.where(d>0,0).rolling(14).mean()
        l=-d.where(d<0,0).rolling(14).mean()
        rsi=100-(100/(1+g/l))
        r=float(rsi.iloc[-1])
        
        av=h['Volume'].tail(20).mean()
        lv=h['Volume'].iloc[-1]
        vol_ratio = lv/av

        if last<=low*1.02 and r<40 and lv>av*0.8:
            return f"""🟢 توصية شراء قوية - {s}
━━━━━━━━━━━━
💰 السعر الحالي: {last:.2f} ({change:+.2f}%)
📉 اقل سعر 20 يوم: {low:.2f}
📈 اعلى سعر 20 يوم: {high:.2f}

📊 RSI(14): {r:.1f} - تشبع بيعي
📦 السيولة: {vol_ratio:.1f}x عن المتوسط
🔎 الحالة: عند القاع + دخول سيولة

🎯 الهدف الأول: {last*1.04:.2f} (+4%)
🎯 الهدف الثاني: {last*1.07:.2f} (+7%)
🛑 وقف الخسارة: {last*0.97:.2f} (-3%)
⏰ المدة: 3-7 ايام
"""
    except:
        pass

send("✅ البوت V3 اشتغل - تفاصيل كاملة + RSI")
while True:
    for s in STOCKS:
        m=check(s)
        if m:
            send(m)
        time.sleep(4)
    time.sleep(300)
