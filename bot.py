import yfinance as yf
import requests
import os
import datetime as dt
BOT=os.getenv("BOT_TOKEN")
CHAT=os.getenv("CHAT_ID")
now=dt.datetime.now()
is_test=(now.minute==0)
def rsi(df):
 try:
  a=df['Close'].diff()
  g=a.where(a>0,0).rolling(14).mean()
  l=-a.where(a<0,0).rolling(14).mean()
  return float(100-(100/(1+g/l)))
 except:
  return 50.0
def get(sym):
 try:
  df=yf.download(sym,period="1mo")
  if len(df)<5:
   return None
  c=float(df['Close'].iloc[-1])
  p=float(df['Close'].iloc[-2])
  ch=(c-p)/p*100
  r=rsi(df)
  lo=float(df['Low'].tail(20).min())
  hi=float(df['High'].tail(20).max())
  t1=c*1.04
  t2=c*1.08
  st=lo*0.98
  if r<30:
   du="2-4 ايام"
  elif r<45:
   du="3-6 ايام"
  elif r>70:
   du="1-2 يوم"
  else:
   du="5-10 ايام"
  return c,ch,r,hi,lo,t1,t2,st,du
 except:
  return None
syms=["2222.SR","2010.SR","1120.SR","META","NVDA","AAPL","BTC-USD","ETH-USD","SOL-USD","EURUSD=X"]
nms=["ارامكو 2222","سابك 2010","الراجحي 1120","META","NVDA","AAPL","BTC","ETH","SOL","EUR/USD"]
mkt=["تاسي","تاسي","تاسي","امريكي","امريكي","امريكي","كريبتو","كريبتو","كريبتو","فوركس"]
if is_test:
 m="✅ البوت شغال تمام\n"
 m+=f"⏰ {now:%H:%M}\n"
 m+="فحص كل ساعة\n"
 m+="بدون توصية"
else:
 m="🔥 توصيات ابو سلطان\n"
 m+=f"⏰ {now:%H:%M} - كل 15 د\n\n"
 for i in range(len(syms)):
  d=get(syms[i])
  if d is None:
   continue
  c,ch,r,hi,lo,t1,t2,st,du=d
  if r<30:
   rec="شراء قوي 🟢"
   pr
