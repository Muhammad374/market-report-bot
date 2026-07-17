import os
import asyncio
import requests
from telegram import Bot

TOKEN = os.environ["BOT_TOKEN"]
CHANNEL = -1003797303512


def safe_get(url):
    try:
        r = requests.get(url, timeout=10)
        return r.json()
    except:
        return None


def get_usdt():
    try:
        data = safe_get("https://api.tetherland.com/currencies")
        return int(data["data"]["currencies"]["USDT"]["price"])
    except:
        return None


def get_crypto():
    try:
        url = (
            "https://api.coingecko.com/api/v3/simple/price"
            "?ids=bitcoin,ethereum&vs_currencies=usd"
        )

        data = safe_get(url)

        return (
            data["bitcoin"]["usd"],
            data["ethereum"]["usd"]
        )

    except:
        return None, None


def get_global_market():
    # فعلاً جای اتصال اونس و نفت
    return None, None


def get_iran_gold():
    # فعلاً جای اتصال طلای ایران و سکه
    return None, None


async def main():

    usdt = get_usdt()
    btc, eth = get_crypto()
    gold, oil = get_global_market()
    gold18, coin = get_iran_gold()


    message = f"""
📊 Goldx Market Report

💵 تتر:
{f"{usdt:,} تومان" if usdt else "نامشخص"}

₿ بیت‌کوین:
{f"${btc:,}" if btc else "نامشخص"}

Ξ اتریوم:
{f"${eth:,}" if eth else "نامشخص"}

🟡 اونس جهانی طلا:
{f"${gold}" if gold else "نامشخص"}

🛢 نفت:
{f"${oil}" if oil else "نامشخص"}

🥇 طلای ۱۸ عیار:
{f"{gold18:,} تومان" if gold18 else "نامشخص"}

🪙 سکه بهار آزادی:
{f"{coin:,} تومان" if coin else "نامشخص"}

⏱ بروزرسانی هر ۱ ساعت
"""


    bot = Bot(token=TOKEN)

    await bot.send_message(
        chat_id=CHANNEL,
        text=message
    )

    print("MESSAGE SENT")


if __name__ == "__main__":
    asyncio.run(main())
