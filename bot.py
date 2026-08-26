import yfinance as yf, requests, os, time
from datetime import datetime, timezone, timedelta

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
GROUP_ID = os.getenv("GROUP_ID")


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
    """يجيب السعر ويحسب RSI. يرجع None لو صار خطأ (بدل ما يرسل قيم فاضية)."""
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
            status, per = "شراء قوي", "80"
            icon = "🟢"
        elif r < 45:
            status, per = "شراء", "60"
            icon = "🟢"
        elif r > 72:
            status, per = "بيع قوي", "80"
            icon = "🔴"
        elif r > 60:
            status, per = "بيع", "60"
            icon = "🔴"
        else:
            status, per = "انتظار", "50"
            icon = "🟡"

        return price, r, status, per, icon

    except Exception as e:
        print(f"[get_recommendation] خطأ: {e}")
        return None


def main():
    result = get_recommendation()

    if result is None:
        # ما نرسل شي إذا فشلت البيانات - بدل ما نرسل توصية بسعر صفر
        print("تم تخطي الإرسال بسبب فشل جلب البيانات")
        return

    price, r, status, per, icon = result

    now = datetime.now(timezone.utc) + timedelta(hours=3)
    time_str = now.strftime("%I:%M %p")

    msg = f"""🔥 توصيات ابو سلطان - {time_str} ⏰

📊 سهم البلاد (SR.6013)
💰 السعر الحالي: {price:.2f}
📈 RSI: {r:.0f}

التوصية: {status} {icon} %{per}

🎯 دخول: {price:.2f}
🎯 هدف 1: {price*1.02:.2f} (+2%)
🛑 وقف: {price*0.98:.2f} (-2%)

⚠️ ليست نصيحة مالية"""

    send(msg)