import os
import asyncio
import json
import subprocess
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


FILE = "last_message.json"


def read_id():

    try:
        with open(FILE, "r") as f:
            return json.load(f)["message_id"]

    except:
        return None



def save_id(message_id):

    with open(FILE, "w") as f:
        json.dump(
            {
                "message_id": message_id
            },
            f
        )



def git_save():

    subprocess.run(
        ["git", "config", "--global", "user.name", "github-actions"]
    )

    subprocess.run(
        ["git", "config", "--global", "user.email", "actions@github.com"]
    )

    subprocess.run(
        ["git", "add", FILE]
    )

    subprocess.run(
        ["git", "commit", "-m", "save message id"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    subprocess.run(
        ["git", "push"]
    )



async def main():

    bot = Bot(TOKEN)


    old_id = read_id()

    print("OLD ID:", old_id)


    if old_id:

        try:

            await bot.delete_message(
                chat_id=CHANNEL,
                message_id=old_id
            )

            print("DELETED")

        except Exception as e:

            print("DELETE ERROR:", e)



    msg = await bot.send_message(
        chat_id=CHANNEL,
        text=MESSAGE
    )


    print("NEW ID:", msg.message_id)


    save_id(
        msg.message_id
    )


    git_save()


    print("DONE")



if __name__ == "__main__":
    asyncio.run(main())
