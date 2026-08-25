import yfinance as yf
import time, requests, os

BOT_TOKEN=os.getenv("BOT_TOKEN")
CHAT_ID=os.getenv("CHAT_ID")
last_heartbeat = time.time()

STOCKS=[
"1120.SR","2222.SR","7010.SR","1180.SR",
"1150.SR","1211.SR","2380.SR","2030.SR",
"1080.SR","1060.SR","1030.SR","1050.SR",
"1210.SR","2350.SR","2280.SR","2180.SR",
"SOFI","NIO","MARA","RIOT","F","SNAP","LCID",
"PLUG","CHPT","NOK","SIRI","T","INTC","PFE",
"BTC-USD","ETH-USD","SOL-USD","XRP-USD",
"DOGE-USD","SHIB-USD","AVAX-USD","DOT-USD",
"LINK-USD","LTC-USD","UNI-USD","PEPE-USD",
"FLOKI-USD","WIF-USD","TRX-USD","BNB-USD"
]

def send(m):
    try:
        requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={m}")
    except: pass

def get_rsi(t):
    try:
        df=yf.download(t, period="1mo", interval="1d", progress=False)
        if len(df)<15: return 50
        delta=df['Close'].diff()
        gain=delta.where(delta>0,0).rolling(14).mean()
        loss=-delta.where(delta<0,0).rolling(14).mean()
        rs=gain/loss
        return 100-(100/(1+rs)).iloc[-1]
    except: return 50

send("البوت بدأ 🚀 - يفحص السوق الآن")

while True:
    # تنبيه كل ساعة انه شغال
    if time.time() - last_heartbeat > 3600:
        send("البوت شغال ✅ - يفحص السوق ...")
        last_heartbeat = time.time()

    for s in STOCKS:
        rsi=get_rsi(s)
        if rsi<35:
            send(f"فرصة دخول 🔥\nالسهم: {s}\nRSI: {round(rsi,1)}\nالسعر: تشييك مباشر")
        time.sleep(3)
    time.sleep(300)
