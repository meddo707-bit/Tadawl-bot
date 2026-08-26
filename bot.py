import yfinance as yf
import requests
import os
import datetime as dt
BOT=os.getenv("BOT_TOKEN")
CHAT=os.getenv("CHAT_ID")
now=dt.datetime.now()
test=now.minute==0
def rsi(d):
 a=d['Close'].diff()
 g=a.where(a>0,0).rolling(14).mean()
 l=-a.where(a<0,0).rolling(14).mean()
 return float(100-(100/(1+g/l)))
def get(s):
 try:
  df=yf.download(s,period="2mo")
  c=float(df['Close'][-1])
  p=float(df['Close'][-2])
  ch=(c-p)/p*100
  r=rsi(df)
  hi=float(df['High'].tail(20).max())
  lo=float(df['Low'].tail(20).min())
  t1=c*1.04
  t2=c*1.08
  st=lo*0.98
  if r<30:
   dur="2-4 ايام"
  elif r<45:
   dur="3-6 ايام"
  elif r>70:
   dur="1-2 يوم"
  else:
   dur="5-10 ايام"
  return c,ch,r,hi,lo,t1,t2,st,dur
 except:
  return None
syms=[
 "2222.SR",
 "2010.SR",
 "1120.SR",
 "META",
 "NVDA",
 "AAPL",
 "BTC-USD",
 "ETH-USD",
 "SOL-USD",
 "EURUSD=X"
]
nms=[
 "ارامكو 2222",
 "سابك 2010",
 "الراجحي 1120",
 "META",
 "NVDA",
 "AAPL",
 "BTC",
 "ETH",
 "SOL",
 "EUR/USD"
]
mk=[
 "تاسي",
 "تاسي",
 "تاسي",
 "امريكي",
 "امريكي",
 "امريكي",
 "كريبتو",
 "كريبتو",
 "كريبتو",
 "فوركس"
]
if test:
 m="✅ البوت شغال تمام\n"
 m+=f"الوقت: {now:%H:%M}\n"
 m+="فحص كل ساعة\n"
 m+="بدون توصية - كل شي تمام"
else:
 m="🔥 توصيات ابو سلطان\n"
 m+=f"⏰ {now:%H:%M} كل 15 د\n\n"
 for i in range(len(syms)):
  d=get(syms[i])
  if not d:
   continue
  c,ch,r,hi,lo,t1,t2,st,dur=d
  if r<30:
   rec="شراء قوي 🟢"
   pc="80%"
  elif r<40:
   rec="شراء 👍"
   pc="65%"
  elif r>75:
   rec="بيع قوي 🔴"
   pc="80%"
  elif r>65:
   rec="جني ربح ⚠️"
   pc="70%"
  else:
   rec="انتظار 🟡"
   pc="50%"
  m+=f"{nms[i]} ({mk[i]})\n"
  m+=f"{rec} قوة {pc}\n"
  m+=f"دخول {c:.2f} {ch:+.1f}%\n"
  m+=f"RSI {r:.0f} | {lo:.1f}-{hi:.1f}\n"
  m+=f"🎯1 {t1:.2f} +4%\n"
  m+=f"🎯2 {t2:.2f} +8%\n"
  m+=f"🛑 {st:.2f} -2%\n"
  m+=f"⏳ {dur}\n\n"
 m+="⚠️ ليست نصيحة مالية"
u=f"https://api.telegram.org/bot{BOT}/sendMessage"
p={"chat_id":CHAT,"text":m}
requests.post(u,data=p)
