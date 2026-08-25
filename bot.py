import yfinance as yf
import time, requests, os

BOT_TOKEN=os.getenv("BOT_TOKEN")
CHAT_ID=os.getenv("CHAT_ID")
last_heartbeat = time.time()

STOCKS=[
"1120.SR","2222.SR","7010.SR","1180.SR","1150.SR","1211.SR",
"SOFI","NIO","MARA","RIOT","F","SNAP","SIRI","T","INTC","PFE",
"BTC-USD","ETH-USD","SOL-USD","XRP-USD","DOGE-USD","SHIB-USD"
]

def send(m):
    try:
        requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={m}", timeout=10)
    except: pass

def get_rsi(t):
    try:
        df=yf.download(t, period="1mo", interval="1d", progress=False, auto_adjust=True)
        if len(df)<15: return 50
        close = df['Close']
        delta=close.diff()
        gain=delta.where(delta>0,0).rolling(14).mean()
        loss=-delta.where(delta<0,0).rolling(14).mean()
        rs=gain/loss
        rsi = 100-(100/(1+rs))
        val = float(rsi.iloc[-1])
        return val
    except Exception as e:
        print(f"Error {t}: {e}")
        return 50

send("البوت بدأ 🚀 - النسخة الجديدة شغالة")

while True:
    if time.time() - last_heartbeat > 3600:
        send("البوت شغال ✅ - يفحص السوق ...")
        last_heartbeat = time.time()

    for s in STOCKS:
        rsi=get_rsi(s)
        print(f"{s} RSI={rsi}")
        if rsi < 35:
            send(f"فرصة دخول 🔥\nالسهم: {s}\nRSI: {round(rsi,1)}")
        time.sleep(2)
    time.sleep(300)
