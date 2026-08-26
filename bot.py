import yfinance as yf,requests,os,datetime as dt
BOT=os.getenv("BOT_TOKEN")
CHAT=os.getenv("CHAT_ID")
IDS=[c.strip() for c in CHAT.split(",") if c.strip()]
now=dt.datetime.now()
test=(now.minute==0)
def rsi(df):
 a=df['Close'].diff()
 g=a.where(a>0,0).rolling(14).mean()
 l=-a.where(a<0,0).rolling(14).mean()
 return float(100-(100/(1+g/l)))
def get(s):
 try:
  df=yf.download(s,period="1mo")
  c=float(df['Close'].iloc[-1])
  p=float(df['Close'].iloc[-2])
  ch=(c-p)/p*100
  r=rsi(df)
  lo=float(df['Low'].tail(20).min())
  hi=float(df['High'].tail(20).max())
  t1=c*1.04
  t2=c*1.08
  st=lo*0.98
  du="2-4 ايام" if r<30 else "3-6 ايام" if r<45 else "1-2 يوم" if r>70 else "5-10 ايام"
  return c,ch,r,hi,lo,t1,t2,st,du
 except:
  return None
syms=["2222.SR","2010.SR","1120.SR","META","NVDA","AAPL","BTC-USD","ETH-USD","SOL-USD","EURUSD=X"]
nms=["ارامكو 2222","سابك 2010","الراجحي 1120","META","NVDA","AAPL","BTC","ETH","SOL","EUR/USD"]
mk=["تاسي","تاسي","تاسي","امريكي","امريكي","امريكي","كريبتو","كريبتو","كريبتو","فوركس"]
if test:
 m=f"✅ البوت شغال تمام\n⏰ {now:%H:%M}\nفحص كل ساعة بدون توصية"
else:
 m=f"🔥 توصيات ابو سلطان\n⏰ {now:%H:%M} كل 15 د\n\n"
 for i in range(len(syms)):
  d=get(syms[i])
  if not d:continue
  c,ch,r,hi,lo,t1,t2,st,du=d
  rec="شراء قوي 🟢" if r<30 else "شراء 👍" if r<40 else "بيع قوي 🔴" if r>75 else "جني ربح ⚠️" if r>65 else "انتظار 🟡"
  pr="80%" if r<30 or r>75 else "65%" if r<40 else "50%"
  m+=f"{nms[i]} ({mk[i]})\n{rec} {pr}\nدخول {c:.2f} {ch:+.1f}% RSI {r:.0f} [{lo:.1f}-{hi:.1f}]\n🎯1 {t1:.2f} +4% 🎯2 {t2:.2f} +8%\n🛑 {st:.2f} -2% ⏳ {du}\n\n"
 m+="⚠️ ليست نصيحة مالية"
u=f"https://api.telegram.org/bot{BOT}/sendMessage"
for cid in IDS:
 requests.post(u,data={"chat_id":cid,"text":m})
