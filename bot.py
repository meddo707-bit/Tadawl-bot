import yfinance as yf, requests, os, time
from datetime import datetime, timezone, timedelta

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
GROUP_ID = os.getenv("GROUP_ID")

CHECK_INTERVAL = 60 * 10      # يفحص كل الأسواق كل 10 دقايق
HEARTBEAT_INTERVAL = 60 * 15  # رسالة تأكيد "شغال" كل 15 دقيقة

# ================== قوائم المراقبة (٢٠ لكل سوق) ==================

SAUDI_STOCKS = {
    "2222.SR": "أرامكو السعودية",
    "1120.SR": "الراجحي",
    "2010.SR": "سابك",
    "7010.SR": "STC",
    "1180.SR": "الأهلي",
    "2350.SR": "كيان السعودية",
    "1150.SR": "الإنماء",
    "1211.SR": "معادن",
    "2280.SR": "المراعي",
    "4030.SR": "البحري",
    "2020.SR": "سافكو",
    "1050.SR": "البنك السعودي الفرنسي",
    "4001.SR": "أسواق العثيم",
    "6013.SR": "سهم البلاد",
    "2380.SR": "بترو رابغ",
    "1010.SR": "الرياض",
    "4200.SR": "الدريس",
    "2270.SR": "سدافكو",
    "4013.SR": "دله للخدمات الصحية",
    "1140.SR": "بنك البلاد",
}

US_STOCKS = {
    "AAPL": "Apple",
    "MSFT": "Microsoft",
    "NVDA": "Nvidia",
    "GOOGL": "Alphabet",
    "AMZN": "Amazon",
    "META": "Meta",
    "TSLA": "Tesla",
    "AVGO": "Broadcom",
    "BRK-B": "Berkshire Hathaway",
    "JPM": "JPMorgan",
    "LLY": "Eli Lilly",
    "V": "Visa",
    "UNH": "UnitedHealth",
    "XOM": "Exxon Mobil",
    "MA": "Mastercard",
    "COST": "Costco",
    "HD": "Home Depot",
    "PG": "Procter & Gamble",
    "NFLX": "Netflix",
    "ORCL": "Oracle",
}

CRYPTO = {
    "BTC-USD": "بيتكوين",
    "ETH-USD": "إيثيريوم",
    "USDT-USD": "تيثر",
    "BNB-USD": "بينانس كوين",
    "SOL-USD": "سولانا",
    "XRP-USD": "ريبل",
    "USDC-USD": "يو إس دي كوين",
    "DOGE-USD": "دوجكوين",
    "ADA-USD": "كاردانو",
    "TRX-USD": "ترون",
    "AVAX-USD": "أفالانش",
    "SHIB-USD": "شيبا",
    "TON-USD": "تون كوين",
    "DOT-USD": "بولكادوت",
    "LINK-USD": "تشين لينك",
    "BCH-USD": "بيتكوين كاش",
    "NEAR-USD": "نير",
    "MATIC-USD": "بوليجون",
    "LTC-USD": "لايتكوين",
    "UNI-USD": "يونيسواب",
}

ALL_MARKETS = {
    "🇸🇦 السوق السعودي": SAUDI_STOCKS,
    "🇺🇸 السوق الأمريكي": US_STOCKS,
    "₿ سوق الكريبتو": CRYPTO,
}


# ================== إرسال تلقرام ==================

def send_to(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
    for attempt in range(1, 4):
        try:
            r = requests.post(url, data=payload, timeout=10)
            if r.status_code == 200:
                return True
            else:
                print(f"[send] فشل - status {r.status_code}: {r.text}")
        except requests.exceptions.RequestException as e:
            print(f"[send] محاولة {attempt} فشلت: {e}")
            time.sleep(3)
    print(f"[send] فشل نهائي لـ {chat_id}")
    return False


def send(text):
    targets = [c for c in (CHAT_ID, GROUP_ID) if c]
    if not targets:
        print("[send] ما فيه CHAT_ID ولا GROUP_ID")
        return False
    ok = True
    for chat_id in targets:
        ok = send_to(chat_id, text) and ok
    return ok


# ================== حساب RSI لرمز واحد ==================

def compute_rsi_signal(close_series):
    """يرجع (price, rsi, status, per, icon) أو None لو فشل الحساب"""
    close = close_series.dropna()
    if len(close) < 15:
        return None

    price = float(close.iloc[-1])
    delta = close.diff()
    gain = delta.where(delta > 0, 0).rolling(14).mean()
    loss = -delta.where(delta < 0, 0).rolling(14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    r = float(rsi.iloc[-1])

    if r < 32:
        status, per, icon, direction = "شراء قوي", "80", "🟢", "buy"
    elif r < 45:
        status, per, icon, direction = "شراء", "60", "🟢", "buy"
    elif r > 72:
        status, per, icon, direction = "بيع قوي", "80", "🔴", "sell"
    elif r > 60:
        status, per, icon, direction = "بيع", "60", "🔴", "sell"
    else:
        status, per, icon, direction = "انتظار", "50", "🟡", "wait"

    return price, r, status, per, icon, direction


# ================== فحص سوق كامل بطلب واحد مجمّع ==================

def scan_market(symbols_dict):
    """يفحص كل رموز سوق معين بطلب واحد. يرجع dict: symbol -> (name, price, r, status, per, icon)"""
    tickers = list(symbols_dict.keys())
    results = {}

    try:
        data = yf.download(tickers, period="1mo", group_by="ticker",
                            progress=False, threads=True)
    except Exception as e:
        print(f"[scan] فشل تحميل الدفعة: {e}")
        return results

    for symbol in tickers:
        try:
            if len(tickers) == 1:
                close = data["Close"]
            else:
                close = data[symbol]["Close"]
            r = compute_rsi_signal(close)
            if r is not None:
                price, rsi, status, per, icon, direction = r
                results[symbol] = (symbols_dict[symbol], price, rsi, status, per, icon, direction)
        except Exception as e:
            print(f"[scan] تخطي {symbol}: {e}")
            continue

    return results


# ================== بناء رسالة التنبيه ==================

def build_alert(market_label, symbol, name, price, r, status, per, icon, direction):
    now = datetime.now(timezone.utc) + timedelta(hours=3)
    time_str = now.strftime("%I:%M %p")

    if direction == "buy":
        # شراء: نتوقع صعود السعر، الهدف فوق والوقف تحت
        target1 = price * 1.02
        target2 = price * 1.04
        stop = price * 0.98
        action_line = f"📥 نوصي بالشراء عند: {price:.2f}"
        targets_line = (
            f"🎯 هدف 1 (ربح متوقع +2%): {target1:.2f}\n"
            f"🎯 هدف 2 (ربح متوقع +4%): {target2:.2f}\n"
            f"🛑 وقف الخسارة (-2%): {stop:.2f}"
        )
    elif direction == "sell":
        # بيع: نتوقع نزول السعر، الهدف تحت والوقف فوق
        target1 = price * 0.98
        target2 = price * 0.96
        stop = price * 1.02
        action_line = f"📤 نوصي بالبيع/جني الأرباح عند: {price:.2f}"
        targets_line = (
            f"🎯 هدف 1 (تجنب خسارة -2%): {target1:.2f}\n"
            f"🎯 هدف 2 (تجنب خسارة -4%): {target2:.2f}\n"
            f"🛑 وقف (لو رجع يصعد +2%): {stop:.2f}"
        )
    else:
        action_line = f"⏸ لا توجد إشارة واضحة حاليًا عند: {price:.2f}"
        targets_line = "انتظر إشارة أوضح قبل الدخول أو الخروج"

    return f"""🔥 توصيات ابو سلطان - {time_str} ⏰

{market_label}
📊 {name} ({symbol})
💰 السعر الحالي: {price:.2f}
📈 مؤشر القوة النسبية RSI: {r:.0f}

📢 التوصية: {status} {icon} (قوة الإشارة {per}%)

{action_line}
{targets_line}

⚠️ ليست نصيحة مالية، القرار النهائي يرجع لك"""


def heartbeat_message(total_watched):
    now = datetime.now(timezone.utc) + timedelta(hours=3)
    time_str = now.strftime("%I:%M %p")
    return f"✅ البوت شغال - {time_str}\n👀 يراقب {total_watched} سهم/عملة"


# ================== الحلقة الرئيسية ==================

def main():
    total = sum(len(m) for m in ALL_MARKETS.values())
    print(f"🚀 البوت بدأ الشغل... يراقب {total} رمز")
    send(f"🚀 البوت اشتغل الحين وبيراقب {total} سهم/عملة (سعودي + أمريكي + كريبتو)")

    last_status = {}   # symbol -> آخر توصية
    last_heartbeat = 0

    while True:
        now_ts = time.time()

        for market_label, symbols_dict in ALL_MARKETS.items():
            print(f"[{datetime.now()}] فحص {market_label}...")
            results = scan_market(symbols_dict)

            for symbol, (name, price, r, status, per, icon, direction) in results.items():
                if last_status.get(symbol) != status:
                    msg = build_alert(market_label, symbol, name, price, r, status, per, icon, direction)
                    send(msg)
                    last_status[symbol] = status
                    print(f"[{datetime.now()}] تنبيه جديد: {name} -> {status}")

            time.sleep(2)  # فاصل بسيط بين الأسواق عشان ما نضغط على yfinance

        # heartbeat كل 15 دقيقة
        if now_ts - last_heartbeat >= HEARTBEAT_INTERVAL:
            send(heartbeat_message(total))
            last_heartbeat = now_ts
            print(f"[{datetime.now()}] تم إرسال heartbeat")

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
