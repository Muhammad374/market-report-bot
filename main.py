import os
import asyncio
import requests
from datetime import datetime
from telegram import Bot

TOKEN = os.environ["BOT_TOKEN"]
CHANNEL = -1003797303512


def get_json(url):
    try:
        r = requests.get(url, timeout=10)
        return r.json()
    except Exception:
        return None


# -------------------------
# Tether تومان
# -------------------------
def get_usdt():
    try:
        data = get_json("https://api.tetherland.com/currencies")
        return int(data["data"]["currencies"]["USDT"]["price"])
    except:
        return None


# -------------------------
# BTC / ETH دلار
# -------------------------
def get_crypto():
    try:
        url = (
            "https://api.coingecko.com/api/v3/simple/price"
            "?ids=bitcoin,ethereum&vs_currencies=usd"
        )

        data = get_json(url)

        return (
            data["bitcoin"]["usd"],
            data["ethereum"]["usd"]
        )

    except:
        return None, None


# -------------------------
# اونس طلا
# -------------------------
def get_gold_ounce():
    # اینجا API اونس قرار می‌گیرد
    return None


# -------------------------
# نفت
# -------------------------
def get_oil():
    # اینجا API نفت قرار می‌گیرد
    return None


# -------------------------
# طلای ۱۸ میلی گلد
# -------------------------
def get_gold18():
    # اینجا API میلی گلد قرار می‌گیرد
    return None


# -------------------------
# سکه
# -------------------------
def get_coin():
    # اینجا API سکه قرار می‌گیرد
    return None



async def main():

    usdt = get_usdt()
    btc, eth = get_crypto()

    ounce = get_gold_ounce()
    oil = get_oil()
    gold18 = get_gold18()
    coin = get_coin()


    time = datetime.now().strftime("%H:%M")


    message = f"""
📊 Goldx Market

━━━━━━━━━━━━

💵 Tether
{f"{usdt:,} تومان" if usdt else "-"}

₿ Bitcoin
{f"${btc:,}" if btc else "-"}

Ξ Ethereum
{f"${eth:,}" if eth else "-"}

━━━━━━━━━━━━

🟡 Gold Ounce
{f"${ounce}" if ounce else "-"}

🛢 Oil
{f"${oil}" if oil else "-"}

🥇 Gold 18K
{f"{gold18:,} تومان" if gold18 else "-"}

🪙 Bahar Azadi Coin
{f"{coin:,} تومان" if coin else "-"}

━━━━━━━━━━━━

🕒 {time}
"""


    bot = Bot(token=TOKEN)

    await bot.send_message(
        chat_id=CHANNEL,
        text=message
    )

    print("MESSAGE SENT")


if __name__ == "__main__":
    asyncio.run(main())
