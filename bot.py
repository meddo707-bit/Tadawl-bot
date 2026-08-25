import yfinance as yf, os, requests
from datetime import datetime

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_IDS = os.getenv("CHAT_ID","").split(",")

STOCKS = ["1120.SR","1211.SR","2222.SR","2010.SR","2280.SR","AAPL","MSFT","NVDA","TSLA","META","BTC-USD","ETH-USD","SOL-USD"]

def get_signal(t):
    try:
        df = yf.download(t, period="1mo", progress=False, auto_adjust=True)
        if len(df) < 21:
            return None
        
        c = df['Close']
        if hasattr(c, 'columns'):
            c = c.iloc[:,0]
        
        p = float(c.iloc[-1])
        low = float(c.min())
        
        d = c.diff()
        g = d.where(d>0,0).rolling(14).mean()
        l = (-d.where(d<0,0)).rolling(14).mean()
        rs = g / l
        rsi = float((100 - (100/(1+rs))).iloc[-1])
        change = float((c.iloc[-1]/c.iloc[-2]-1)*100)
        
        if rsi < 70 and p <= low * 1.18:
            market = "🇸🇦 تاسي" if ".SR" in t else "🪙 كريبتو" if "-USD" in t else "🇺🇸 امريكي"
            name = t.replace(".SR","").replace("-USD","")
            return f"🟢 {name} - {market}\nالسعر: {p:.2f} | RSI: {rsi:.0f} | {change:+.1f}%\nقريب من القاع"
    except Exception as e:
        print(f"Error {t}: {e}")
        return None
    return None

now = datetime.now().strftime("%I:%M %p - %d/%m")
msgs = [s for s in [get_signal(x) for x in STOCKS] if s]

if msgs:
    text = f"🔥 توصيات ابو سلطان - {now} 🔥\n\n" + "\n\n".join(msgs)
else:
    text = f"✅ فحص لايف - {now}\nلا يوجد فرص قوية حاليا\nالفحص كل 30 دقيقة تلقائيا"

for cid in CHAT_IDS:
    cid = cid.strip()
    if cid:
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data={"chat_id":cid,"text":text})

print(text)
