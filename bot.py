import yfinance as yf, os, requests
from datetime import datetime

BOT_TOKEN=os.getenv("BOT_TOKEN")
CHAT_IDS=os.getenv("CHAT_ID","").split(",")

STOCKS = ["1120.SR","1211.SR","2222.SR","2010.SR","2280.SR","1120.SR","1211.SR","AAPL","MSFT","NVDA","TSLA","META","AMZN","GOOGL","BTC-USD","ETH-USD","SOL-USD","XRP-USD","DOGE-USD"]

def get_signal(t):
    try:
        df=yf.download(t, period="1mo", progress=False, auto_adjust=True)
        if len(df)<21: return None
        c=df['Close']
        if isinstance(c, yf.data.frame.DataFrame) if hasattr(c,'columns') else False:
            c=c.iloc[:,0]
        # لو MultiIndex
        try:
            c=c.droplevel(1, axis=1) if hasattr(c,'columns') else c
        except: pass
        
        p=float(c.iloc[-1])
        low=float(c.min())
        high=float(c.max())
        
        # RSI
        d=c.diff()
        g=d.where(d>0,0).rolling(14).mean()
        l=(-d.where(d<0,0)).rolling(14).mean()
        rs=g/l
        rsi=float((100-(100/(1+rs))).iloc[-1])
        
        change=float((c.iloc[-1]/c.iloc[-2]-1)*100)
        
        if rsi < 70 and p <= low*1.15:
            market="🇸🇦 تاسي" if ".SR" in t else "🇺🇸 امريكي" if "-USD" not in t else "🪙 كريبتو"
            name=t.replace(".SR","").replace("-USD","")
            emoji="🟢"
            return f"{emoji} {name} - {market}\nالسعر: {p:.2f} | RSI: {rsi:.0f} | تغير: {change:+.1f}%\nقريب من القاع - فرصة دخول"
    except Exception as e:
        print(f"Error {t}: {e}")
        return None
    return None

now = datetime.now().strftime("%I:%M %p - %d/%m")
msgs=[s for s in [get_signal(x) for x in STOCKS] if s]

if msgs:
    text=f"🔥 توصيات ابو سلطان - {now} 🔥\n\n" + "\n\n".join(msgs)
else:
    text=f"✅ فحص لايف - {now}\nلا يوجد فرص قوية حاليا قريبة من القاع\nسيتم الفحص تلقائيا كل 30 دقيقة"

for cid in CHAT_IDS:
    if cid.strip():
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data={"chat_id":cid.strip(),"text":text})

print(text)
