import os
import asyncio
import json
from telegram import Bot


TOKEN = os.environ["BOT_TOKEN"]
CHANNEL = -1003797303512


message = """
📊 Goldx Market

💵 دلار (USDT)

191,700 تومان

━━━━━━━━━━━━

₿ بیت‌کوین (BTC)

63,980 دلار

Ξ اتریوم (ETH)

1,837 دلار

━━━━━━━━━━━━

📡 Goldx Live Market
"""


def get_old_message():
    try:
        with open("last_message.json", "r") as f:
            data = json.load(f)
            return data["message_id"]
    except:
        return None


def save_message(message_id):
    with open("last_message.json", "w") as f:
        json.dump(
            {
                "message_id": message_id
            },
            f
        )


async def main():

    bot = Bot(token=TOKEN)

    old_id = get_old_message()

    if old_id:
        try:
            await bot.delete_message(
                chat_id=CHANNEL,
                message_id=old_id
            )
        except Exception as e:
            print(e)


    new_message = await bot.send_message(
        chat_id=CHANNEL,
        text=message
    )


    save_message(
        new_message.message_id
    )


    print("DONE")


if __name__ == "__main__":
    asyncio.run(main())
