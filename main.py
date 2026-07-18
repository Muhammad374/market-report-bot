import os
import json
import asyncio
import requests
from datetime import datetime
from telegram import Bot


# =========================
# SETTINGS
# =========================

TOKEN = os.environ["BOT_TOKEN"]

CHANNEL = int(
    os.environ.get(
        "CHANNEL_ID",
        "-1003797303512"
    )
)

NAVASAN_KEY = os.environ["NAVASAN_KEY"]


CACHE_FILE = "cache.json"
MESSAGE_FILE = "last_message.json"



# =========================
# FILE FUNCTIONS
# =========================

def read_file(name, default):

    try:
        with open(
            name,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    except:

        return default



def write_file(name, data):

    with open(
        name,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=2
        )



# =========================
# CACHE
# =========================

def get_cache():

    return read_file(
        CACHE_FILE,
        {
            "gold18": None,
            "coin": None,
            "ounce": None,
            "bubble": None,
            "time": 0
        }
    )



def save_cache(data):

    write_file(
        CACHE_FILE,
        data
    )



# =========================
# MESSAGE ID
# =========================

def get_message_id():

    data = read_file(
        MESSAGE_FILE,
        {
            "id": None
        }
    )

    return data["id"]



def save_message_id(message_id):

    write_file(
        MESSAGE_FILE,
        {
            "id": message_id
        }
    )



# =========================
# SAFE REQUEST
# =========================

def request_json(url, headers=None):

    try:

        r = requests.get(
            url,
            headers=headers,
            timeout=15
        )

        return r.json()

    except Exception as e:

        print(
            "REQUEST ERROR:",
            e
        )

        return None



# =========================
# NUMBER FORMAT
# =========================

def money(value):

    try:

        return f"{int(value):,}"

    except:

        return "-"



def percent(value):

        return ""



# =========================
# GOLD FORMULA
# =========================

def gold_real_price(ounce, usdt):

    try:

        # اونس ریالی → اونس دلاری
        ounce_usd = ounce / usdt

        # هر گرم طلای 24 عیار به تومان
        gram24 = (ounce_usd / 31.1035) * usdt

        # تبدیل 24 عیار به 18 عیار
        gram18 = gram24 * 18 / 24

        return int(gram18)

    except Exception as e:

        print(
            "GOLD FORMULA ERROR:",
            e
        )

        return None




# =========================
# TIME CHECK
# =========================

def gold_update_needed(cache):

    now = datetime.now().timestamp()

    return (
        now - cache["time"]
        >
        7 * 3600
    )
# =========================
# USDT
# =========================

def get_usdt():

    try:

        data = request_json(
            "https://api.tetherland.com/currencies"
        )

        return int(
            data["data"]["currencies"]["USDT"]["price"]
        )

    except Exception as e:

        print(
            "USDT ERROR:",
            e
        )

        return None



# =========================
# BTC / ETH
# =========================

def get_crypto():

    try:

        url = (
            "https://api.coingecko.com/api/v3/simple/price"
            "?ids=bitcoin,ethereum"
            "&vs_currencies=usd"
            "&include_24hr_change=true"
        )


        data = request_json(url)


        return {

            "btc":
                data["bitcoin"]["usd"],

            "btc_change":
                data["bitcoin"]["usd_24h_change"],


            "eth":
                data["ethereum"]["usd"],

            "eth_change":
                data["ethereum"]["usd_24h_change"]

        }


    except Exception as e:

        print(
            "CRYPTO ERROR:",
            e
        )


        return {

            "btc": None,
            "btc_change": None,
            "eth": None,
            "eth_change": None

        }



# =========================
# NAVASAN
# =========================

def get_navasan():

    try:

        url = (
            "http://api.navasan.tech/latest/"
            "?api_key="
            + NAVASAN_KEY
        )


        data = request_json(url)

        print(data)


        return {

            "gold18":
                int(data["18ayar"]["value"]),


            "coin":
                int(data["bahar"]["value"]),


            "ounce":
                int(data["xau"]["value"]),


            "bubble":
                int(data["bub_18ayar"]["value"])

        }


    except Exception as e:

        print(
            "NAVASAN ERROR:",
            e
        )

        return None



# =========================
# UPDATE GOLD CACHE
# =========================

def update_gold(cache):


    if gold_update_needed(cache):


        data = get_navasan()


        if data:


            cache["gold18"] = data["gold18"]

            cache["coin"] = data["coin"]

            cache["ounce"] = data["ounce"]

            cache["bubble"] = data["bubble"]


            cache["time"] = (
                datetime.now().timestamp()
            )


            save_cache(cache)


    return cache


# =========================
# OIL (BRENT)
# =========================

def get_oil():

    try:

        url = (
            "https://api.oilpriceapi.com/v1/prices/latest"
        )

        headers = {
            "Authorization": "Token " + OIL_API_KEY,
            "Content-Type": "application/json"
        }

        data = request_json(
            url,
            headers=headers
        )

        return float(
            data["data"]["BRENT"]["price"]
        )


    except Exception as e:

        print(
            "OIL ERROR:",
            e
        )

        return None



# =========================
# BUILD MESSAGE
# =========================

def build_message(
    usdt,
    crypto,
    cache,
    oil
):


    real = gold_real_price(
        cache["ounce"],
        usdt
    )


    bubble = None

    if cache["gold18"] and real:

        bubble = (
            cache["gold18"]
            -
            real
        )


    text = f"""
📊 Goldx Market

💵 دلار (USDT):{money(usdt)} تومان
.....
₿ بیت‌کوین (BTC):
{money(crypto['btc'])} دلار
{percent(crypto['btc_change'])}
 اتریوم (ETH)
{money(crypto['eth'])} دلار
{percent(crypto['eth_change'])}
.....
🟡 اونس طلا (XAU)
{money(cache['ounce'])} دلار
🛢 نفت (OIL)
{money(oil)}
.....
🥇 طلای ۱۸ عیار
💰 قیمت بازار:
{money(cache['gold18'])} تومان
⚖️ قیمت واقعی:
{money(real)} تومان
🔥 حباب:
{money(bubble)} تومان
.....
🪙 سکه بهار آزادی
💰 قیمت:
{money(cache['coin'])} تومان
🔥 حباب سکه:
{money(cache['bubble'])} تومان
.....
📡 Goldx Live
"""


    return text



# =========================
# SEND TELEGRAM
# =========================

async def send_message(text):


    bot = Bot(
        token=TOKEN
    )


    old = get_message_id()
    
    print("OLD ID:", old)


    if old:

        try:
            print("TRY DELETE:", old)
            
            await bot.delete_message(
                chat_id=CHANNEL,
                message_id=old
            )


            print(
                "OLD MESSAGE DELETED"
            )


        except Exception as e:

            print(
                "DELETE ERROR:",
                e
            )


    new = await bot.send_message(

        chat_id=CHANNEL,

        text=text

    )


    save_message_id(
        new.message_id
    )


    print(
        "MESSAGE SENT:",
        new.message_id
    )




# =========================
# MAIN
# =========================

async def main():

    print(
        "START"
    )


    cache = get_cache()


    usdt = get_usdt()

    print(
        "USDT:",
        usdt
    )


    crypto = get_crypto()

    print(
        "CRYPTO OK"
    )


    cache = update_gold(
        cache
    )


    print(
        "GOLD OK"
    )


    message = build_message(

        usdt,

        crypto,

        cache,

        get_oil()

    )


    print(
        "MESSAGE READY"
    )


    await send_message(
        message
    )


    print(
        "DONE"
    )



if __name__ == "__main__":

    asyncio.run(main())
