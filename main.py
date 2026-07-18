import os
print("FILE START")
import json
import asyncio
import requests
from datetime import datetime
from telegram import Bot

# ==========================
# تنظیمات
# ==========================

TOKEN = os.environ["BOT_TOKEN"]
CHANNEL = -1003797303512

NAVASAN_KEY = os.environ["NAVASAN_KEY"]

CACHE_FILE = "cache.json"
MESSAGE_FILE = "last_message.json"

# ==========================
# توابع فایل
# ==========================

def load_json(file_name, default):

    try:
        with open(file_name, "r", encoding="utf-8") as f:
            return json.load(f)

    except:
        return default


def save_json(file_name, data):

    with open(file_name, "w", encoding="utf-8") as f:

        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=4
        )


# ==========================
# کش قیمت طلا
# ==========================

def load_cache():

    return load_json(
        CACHE_FILE,
        {
            "gold18": None,
            "coin": None,
            "ounce": None,
            "bubble": None,
            "last_update": 0
        }
    )


def save_cache(data):

    save_json(
        CACHE_FILE,
        data
    )


# ==========================
# ذخیره آیدی پیام
# ==========================

def load_message():

    data = load_json(
        MESSAGE_FILE,
        {
            "message_id": None
        }
    )

    return data["message_id"]


def save_message(message_id):

    save_json(
        MESSAGE_FILE,
        {
            "message_id": message_id
        }
    )


# ==========================
# درخواست امن
# ==========================

def get_json(url, headers=None):

    try:

        r = requests.get(
            url,
            headers=headers,
            timeout=15
        )

        if r.status_code == 200:

            return r.json()

    except Exception as e:

        print(e)

    return None


# ==========================
# محاسبه قیمت ذاتی طلا
# ==========================

def real_gold_price(ounce, usdt):

    try:

        return int(
            (ounce * usdt) / 8.999 / 4.6
        )

    except:

        return None


# ==========================
# درصد تغییر
# ==========================

def change_icon(value):

    if value is None:

        return ""

    if value > 0:

        return f"🟢 ▲ {value:.2f}%"

    elif value < 0:

        return f"🔴 ▼ {abs(value):.2f}%"

    return "⚪️"


# ==========================
# آیا باید نوسان آپدیت شود؟
# هر 7 ساعت
# ==========================

def need_update(cache):

    now = datetime.now().timestamp()

    return (
        now - cache["last_update"]
    ) > (7 * 3600)
    # ==========================
# تتر
# ==========================

def get_usdt():

    try:

        data = get_json(
            "https://api.tetherland.com/currencies"
        )

        return int(
            data["data"]["currencies"]["USDT"]["price"]
        )

    except Exception as e:

        print("USDT ERROR:", e)

        return None



# ==========================
# بیت کوین و اتریوم
# ==========================

def get_crypto():

    try:

        url = (
            "https://api.coingecko.com/api/v3/simple/price"
            "?ids=bitcoin,ethereum"
            "&vs_currencies=usd"
            "&include_24hr_change=true"
        )


        data = get_json(url)


        return {

            "btc": data["bitcoin"]["usd"],

            "btc_change":
                data["bitcoin"]["usd_24h_change"],


            "eth": data["ethereum"]["usd"],

            "eth_change":
                data["ethereum"]["usd_24h_change"]

        }


    except Exception as e:

        print("CRYPTO ERROR:", e)

        return {

            "btc": None,
            "btc_change": None,
            "eth": None,
            "eth_change": None

        }



# ==========================
# اونس طلا
# ==========================

def get_ounce():

    try:

        url = (
            "https://www.goldapi.io/api/XAU/USD"
        )


        headers = {

            "x-access-token":
                os.environ["GOLD_API_KEY"],

            "Content-Type":
                "application/json"

        }


        data = get_json(
            url,
            headers
        )


        return data["price"]


    except Exception as e:

        print("GOLD ERROR:", e)

        return None




# ==========================
# نفت
# ==========================

def get_oil():

    try:

        # فعلاً منبع عمومی نفت
        # در صورت تغییر API فقط این قسمت عوض می‌شود

        url = (
            "https://api.marketstack.com/v1/eod/latest"
        )


        return None


    except:

        return None




# ==========================
# نوسان
# طلای 18 و سکه
# ==========================

def get_navasan():

    try:

        url = (
            "http://api.navasan.tech/latest/"
            "?api_key="
            + NAVASAN_KEY
        )


        data = get_json(url)


        return {

            "gold18":
                int(data["18ayar"]["value"]),


            "coin":
                int(data["bahar"]["value"]),


            "ounce":
                int(data["xau"]["value"]),


            "bubble_gold":
                int(data["bub_18ayar"]["value"]),


            "bubble_coin":
                int(data["bub_bahar"]["value"])

        }


    except Exception as e:

        print("NAVASAN ERROR:", e)

        return None



# ==========================
# آپدیت کش طلا
# ==========================

def update_gold_cache(cache):


    if need_update(cache):


        data = get_navasan()


        if data:


            cache["gold18"] = data["gold18"]

            cache["coin"] = data["coin"]

            cache["ounce"] = data["ounce"]

            cache["bubble"] = data["bubble_gold"]

            cache["last_update"] = (
                datetime.now().timestamp()
            )


            save_cache(cache)


    return cache
    # ==========================
# ساخت پیام
# ==========================

def build_message(
    usdt,
    crypto,
    cache,
    ounce,
    oil
):


    real_price = real_gold_price(
        cache["ounce"],
        usdt
    )


    bubble = None


    if cache["gold18"] and real_price:

        bubble = (
            cache["gold18"]
            -
            real_price
        )



    text = f"""
📊 Goldx Market


💵 دلار (USDT)

{f"{usdt:,} تومان" if usdt else "-"}


┌────────────────────┐


₿ بیت‌کوین (BTC)

{f"{crypto['btc']:,} دلار {change_icon(crypto['btc_change'])}" if crypto['btc'] else "-"}


Ξ اتریوم (ETH)

{f"{crypto['eth']:,} دلار {change_icon(crypto['eth_change'])}" if crypto['eth'] else "-"}


━━━━━━━━━━━━━━━━


🟡 اونس طلا (XAU)

{f"{cache['ounce']:,} دلار" if cache['ounce'] else "-"}


🛢 نفت (WTI)

{oil if oil else "-"}


━━━━━━━━━━━━━━━━


🥇 طلای ۱۸ عیار


💰 قیمت بازار:

{f"{cache['gold18']:,} تومان" if cache['gold18'] else "-"}


⚖️ قیمت ذاتی:

{f"{real_price:,} تومان" if real_price else "-"}


🔥 حباب:

{f"{bubble:+,} تومان" if bubble else "-"}


━━━━━━━━━━━━━━━━


🪙 سکه بهار آزادی


💰 قیمت:

{f"{cache['coin']:,} تومان" if cache['coin'] else "-"}


🔥 حباب سکه:

{f"{cache['bubble']:,} تومان" if cache['bubble'] else "-"}


└────────────────────┘


📡 Goldx Live Market
"""


    return text




# ==========================
# ارسال تلگرام
# ==========================

async def send_report(message):


    bot = Bot(
        token=TOKEN
    )


    old_id = load_message()


    if old_id:


        try:

            await bot.delete_message(
                chat_id=CHANNEL,
                message_id=old_id
            )


        except Exception as e:

            print(
                "DELETE ERROR:",
                e
            )



    new = await bot.send_message(

        chat_id=CHANNEL,

        text=message

    )


    save_message(
        new.message_id
    )


    print(
        "MESSAGE SENT:",
        new.message_id
    )




#
