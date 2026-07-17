import os
import asyncio
import requests
from telegram import Bot

TOKEN = os.environ["BOT_TOKEN"]
CHANNEL = -1003797303512


def get_usdt():
    url = "https://api.tetherland.com/currencies"

    r = requests.get(url, timeout=10)
    data = r.json()

    usdt = data["data"]["currencies"]["USDT"]["price"]

    return int(usdt)


async def main():
    usdt_price = get_usdt()

    message = f"""
📊 Goldx Market Report

💵 تتر:
{usdt_price:,} تومان

⏱ بروزرسانی خودکار فعال است
"""

    bot = Bot(token=TOKEN)

    await bot.send_message(
        chat_id=CHANNEL,
        text=message
    )

    print("MESSAGE SENT")


if __name__ == "__main__":
    asyncio.run(main())
