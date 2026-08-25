import yfinance as yf
import requests
import os
BOT_TOKEN=os.getenv("BOT_TOKEN")
CHAT_ID=os.getenv("CHAT_ID")
def calc_rsi(d):
 delta=d['Close'].diff()
 g=delta.where(delta>0,0).rolling(14).mean()
 l=-delta.where(delta<0,0).rolling(14).mean()
 rs=g/l
 rsi=100-(100/(1+rs))
 return rsi.iloc[-1]
def get_info(s):
 try:
  df=yf.download(s,period="1mo",progress=False)
  if df.empty: return None
  c=float(df['Close'].iloc[-1])
  p=float(df['Close'].iloc[-2])
  ch=(c-p)/p*100
  r=float(calc_rsi(df))
  lo=float(df['Low'].tail(20).min())
  tg=c*1.05
  st=lo*0.97
  return c,ch,r,lo,tg,st
 except:
  return None
stocks=["2222.SR","2010.SR","META","NVDA","BTC-USD","ETH-USD","SOL-USD"]
names=["2222 تاسي","2010 تاسي","META امريكي","NVDA امريكي","BTC كريبتو","ETH كريبتو","SOL كريبتو"]
m="توصيات ابو سلطان\n\n"
for i in range(len(stocks)):
 d=get_info(stocks[i])
 if not d: continue
 c,ch,r,lo,tg,st=d
 m+=names[i]+"\n"
 m+=f"{c:.2f} ({ch:.2f}%)\n"
 m+=f"RSI {r:.1f} قاع {lo:.2f}\n"
 m+=f"هدف {tg:.2f} وقف {st:.2f}\n\n"
m+="فحص لايف"
url=f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
requests.post(url,data={"chat_id":CHAT_ID,"text":m})
print(m)
