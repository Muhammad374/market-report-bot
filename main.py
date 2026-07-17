import os
import asyncio
import json
from telegram import Bot


TOKEN = os.environ["BOT_TOKEN"]
CHANNEL = -1003797303512


MESSAGE = """
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


def read_message_id():
    try:
        with open("last_message.json", "r") as file:
            data = json.load(file)
            return data.get("message_id")
    except Exception:
        return None


def write_message_id(message_id):
    with open("last_message.json", "w") as file:
        json.dump(
            {
                "message_id": message_id
            },
            file
        )


async def main():

    bot = Bot(token=TOKEN)


    # پیام قبلی
    old_message_id = read_message_id()

    print("OLD ID:", old_message_id)


    if old_message_id:

        try:
            await bot.delete_message(
                chat_id=CHANNEL,
                message_id=old_message_id
            )

            print("OLD MESSAGE DELETED")

        except Exception as error:

            print(
                "DELETE ERROR:",
                error
            )


    # پیام جدید
    new_message = await bot.send_message(
        chat_id=CHANNEL,
        text=MESSAGE
    )


    print(
        "NEW ID:",
        new_message.message_id
    )


    # ذخیره آیدی پیام جدید
    write_message_id(
        new_message.message_id
    )


    print("DONE")


if __name__ == "__main__":
    asyncio.run(main())
