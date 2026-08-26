import yfinance as yf, requests, os, time
from datetime import datetime, timezone, timedelta

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
GROUP_ID = os.getenv("GROUP_ID")

CHECK_INTERVAL = 60 * 3      # يفحص السهم كل 3 دقايق
HEARTBEAT_INTERVAL = 60 * 15  # رسالة تأكيد "شغال" كل 15 دقيقة


def send(text):
    """يرسل الرسالة لتلقرام. يحاول 3 مرات مع timeout عشان ما يعلق البوت."""
    chat = GROUP_ID or CHAT_ID
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat, "text": text, "parse_mode": "HTML"}

    for attempt in range(1, 4):
        try:
            r = requests.post(url, data=payload, timeout=10)
            if r.status_code == 200:
                return True
            else:
                print(f"[send] فشل الإرسال - status {r.status_code}: {r.text}")
        except requests.exceptions.RequestException as e:
            print(f"[send] محاولة {attempt} فشلت: {e}")
            time.sleep(3)

    print("[send] فشل الإرسال نهائيًا بعد 3 محاولات")
    return False


def get_recommendation():
    """يجيب السعر ويحسب RSI. يرجع None لو صار خطأ."""
    try:
        data = yf.download("6013.SR", period="5d", progress=False)
        close = data['Close'].dropna()

        if close.empty:
            print("[data] ما رجعت بيانات من yfinance")
            return None

        price = float(close.iloc[-1])

        delta = close.diff()
        gain = delta.where(delta > 0, 0).rolling(14).mean()
        loss = -delta.where(delta < 0, 0).rolling(14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        r = float(rsi.iloc[-1])

        if r < 32:
            status, per, icon = "شراء قوي", "80", "🟢"
        elif r < 45:
            status, per, icon = "شراء", "60", "🟢"
        elif r > 72:
            status, per, icon = "بيع قوي", "80", "🔴"
        elif r > 60:
            status, per, icon = "بيع", "60", "🔴"
        else:
            status, per, icon = "انتظار", "50", "🟡"

        return price, r, status, per, icon

    except Exception as e:
        print(f"[get_recommendation] خطأ: {e}")
        return None


def build_message(price, r, status, per, icon):
    now = datetime.now(timezone.utc) + timedelta(hours=3)
    time_str = now.strftime("%I:%M %p")

    return f"""🔥 توصيات ابو سلطان - {time_str} ⏰

📊 سهم البلاد (SR.6013)
💰 السعر الحالي: {price:.2f}
📈 RSI: {r:.0f}

التوصية: {per}% {icon} {status}

🎯 دخول: {price:.2f}
🎯 هدف 1: {price*1.02:.2f} (+2%)
🛑 وقف: {price*0.98:.2f} (-2%)

⚠️ ليست نصيحة مالية"""


def heartbeat_message():
    now = datetime.now(timezone.utc) + timedelta(hours=3)
    time_str = now.strftime("%I:%M %p")
    return f"✅ البوت شغال - {time_str}"


def main():
    print("🚀 البوت بدأ الشغل...")
    send("🚀 البوت اشتغل الحين وبيراقب السهم")

    last_status = None
    last_heartbeat = 0

    while True:
        now_ts = time.time()

        # 1) فحص التوصية
        result = get_recommendation()
        if result is not None:
            price, r, status, per, icon = result

            # يرسل فقط لو التوصية جديدة أو تغيرت عن آخر مرة
            if status != last_status:
                msg = build_message(price, r, status, per, icon)
                send(msg)
                last_status = status
                print(f"[{datetime.now()}] تم إرسال توصية جديدة: {status}")
            else:
                print(f"[{datetime.now()}] لا تغيير بالتوصية ({status}) - ما نرسل")
        else:
            print(f"[{datetime.now()}] فشل جلب البيانات هذي الدورة")

        # 2) رسالة "شغال" كل 15 دقيقة بغض النظر عن التوصية
        if now_ts - last_heartbeat >= HEARTBEAT_INTERVAL:
            send(heartbeat_message())
            last_heartbeat = now_ts
            print(f"[{datetime.now()}] تم إرسال رسالة heartbeat")

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
