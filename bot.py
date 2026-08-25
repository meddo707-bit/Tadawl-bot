import yfinance as yf
import requests
import os
BOT=os.getenv("BOT_TOKEN")
CHAT=os.getenv("CHAT_ID")

def rsi(d):
 a=d['Close'].diff()
 g=a.where(a>0,0).rolling(14).mean()
 l=-a.where(a<0,0).rolling(14).mean()
 return 100-(100/(1+g/l))

def info(s):
 try:
  df=yf.download(s,period="1mo")
  if df.empty:
   return None
  c=float(df['Close'][-1])
  p=float(df['Close'][-2])
  ch=(c-p)/p*100
  r=float(rsi(df))
  lo=float(df['Low'].tail(20).min())
  tg=c*1.05
  st=lo*0.97
  return c,ch,r,lo,tg,st
 except:
  return None

syms=[
"2222.SR",
"2010.SR",
"META",
"NVDA",
"BTC-USD",
"ETH-USD",
"SOL-USD"
]

nms=[
"2222",
"2010",
"META",
"NVDA",
"BTC",
"ETH",
"SOL"
]

m="Bot\n\n"
for i in range(7):
 d=info(syms[i])
 if not d:
  continue
 c,ch,r,lo,tg,st=d
 m+=nms[i]+"\n"
 m+=f"{c:.2f} {ch:.2f}%\n"
 m+=f"RSI {r:.1f}\n"
 m+=f"T {tg:.2f} S {st:.2f}\n\n"

m+="Live"
url=f"https://api.telegram.org/bot{BOT}/sendMessage"
requests.post(url,data={"chat_id":CHAT,"text":m})
print(m)
