import yfinance as yf, os, requests
from datetime import datetime

BOT_TOKEN=os.getenv("BOT_TOKEN")
CHAT_IDS=os.getenv("CHAT_ID","").split(",")
now = datetime.now().strftime("%I:%M %p - %d/%m")

STOCKS = [
"1120.SR","1211.SR","2222.SR","2010.SR","2280.SR","1180.SR","1150.SR","1320.SR","2380.SR","2310.SR",
"AAPL","MSFT","NVDA","TSLA","META","AMZN","GOOGL","NFLX","AMD","PLTR",
"BTC-USD","ETH-USD","SOL-USD","XRP-USD","DOGE-USD","SHIB-USD","PEPE-USD","BONK-USD","AVAX-USD","LINK-USD"
]

def get_signal(t):
    try:
        df=yf.download(t, period="1mo", progress=False, auto_adjust=True)
        if len(df)<21: return None
        c=df['Close']; p=float(c.iloc[-1]); low=float(c.tail(20).min())
        d=c.diff(); g=d.where(d>0,0).rolling(14).mean(); l=-d.where(d<0,0).rolling(14).mean()
        rsi=float((100-(100/(1+g/l))).iloc[-1])
        
        change=float((c.iloc[-1]/c.iloc[-2]-1)*100)
        
        if rsi < 70 and p <= low*1.15:
            market="🇸🇦 تاسي" if ".SR" in t else "₿ كريبتو" if "-USD" in t else "🇺🇸 وول ستريت"
            return f"🟢 {t.replace('.SR','').replace('-USD','')} - {market}\n💰 {p:.4f} ({change:+.2f}%)\n📊 RSI: {rsi:.1f} | قاع 20ي: {low:.4f}\n🎯 هدف: {p*1.05:.4f} (+5%) | وقف: {low*0.97:.4f}\n⏰ {now}"
    except: return None
    return None

msgs=[s for s in [get_signal(x) for x in STOCKS] if s]

if msgs:
    text=f"🔥 توصيات ابو سلطان - {now} 🔥\n\n"+"\n\n---\n\n".join(msgs[:8])+"\n\n✅ فحص لايف مباشر"
else:
    text=f"✅ فحص لايف - {now}\nالسوق مرتفع - لا فرص قوية حاليا\n📊 تم فحص 30 سهم لايف\n⏰ القادم بعد 30 دقيقة"

for cid in CHAT_IDS:
    if cid.strip():
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data={"chat_id":cid.strip(),"text":text}, timeout=20)
