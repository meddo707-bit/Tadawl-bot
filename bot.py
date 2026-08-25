import os, time, requests, yfinance as yf, pandas as pd
BOT_TOKEN=os.getenv("BOT_TOKEN")
CHAT_ID=os.getenv("CHAT_ID")
STOCKS=["BB","SIRI","PLUG","SOFI","NOK","AMC","GME","SPCE","NIO","XPEV","LCID","RIVN","F","T","WBD","PARA","INTC","PFE","CCL","NCLH","AAL","UAL","DAL","SNAP","PINS","HOOD","DKNG","OPEN","RKT"]

def send(m):
    try:
        requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", params={"chat_id":CHAT_ID,"text":m}, timeout=20)
        print(f"Sent: {m[:30]}")
    except Exception as e:
        print(e)

def get_rsi(s, p=14):
    d=s.diff(); g=d.where(d>0,0).rolling(p).mean(); l=(-d.where(d<0,0)).rolling(p).mean()
    rs=g/l; return 100-(100/(1+rs))

send("✅ اشتغل البوت - جاري فحص 30 سهم الآن...")

while True:
    try:
        found=0
        for sym in STOCKS:
            try:
                df=yf.download(sym, period="3mo", interval="1d", progress=False, auto_adjust=True)
                if len(df)<25: continue
                close=df['Close']
                if isinstance(close, pd.DataFrame): close=close.iloc[:,0]
                rsi_val=get_rsi(close).iloc[-1]
                price=float(close.iloc[-1])
                low20=float(close.tail(20).min())
                if isinstance(rsi_val, pd.Series): rsi_val=float(rsi_val.iloc[-1])

                if rsi_val < 35 and price <= low20*1.10:
                    msg=f"🟢 فرصة دخول\n🇺🇸 {sym} - وول ستريت\n\n🏢 {sym}\n💰 السعر: $ {price:.4f}\n📊 RSI: {rsi_val:.1f}\n📉 قاع 20 يوم: {low20:.4f}\n\n🎯 هدف 1: {price*1.04:.4f} (+4%)\n🎯 هدف 2: {price*1.08:.4f} (+8%)\n🛑 وقف: {low20*0.97:.4f}"
                    send(msg)
                    found+=1
                    time.sleep(2)
            except Exception as e:
                print(f"{sym} error {e}")
                continue
        
        if found==0:
            send(f"🔍 فحصت 30 سهم - RSI كلها فوق 35، ما فيه فرص قوية الآن - الساعة {time.strftime('%H:%M')}")

        time.sleep(600) # كل 10 دقايق
    except Exception as e:
        print(e)
        time.sleep(60)
