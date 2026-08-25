import yfinance as yf, os, requests
BOT_TOKEN=os.getenv("BOT_TOKEN")
CHAT_IDS=os.getenv("CHAT_ID","").split(",")
for cid in CHAT_IDS:
  requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data={"chat_id":cid.strip(),"text":"✅ البوت رجع يشتغل - فحص تجريبي"})
