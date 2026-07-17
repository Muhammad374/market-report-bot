import os
import asyncio
from telegram import Bot

TOKEN = os.environ["BOT_TOKEN"]

CHANNEL = -1003797303512

message = """
📊 گزارش تست بازار

🟡 طلا: در حال دریافت...
₿ بیت‌کوین: در حال دریافت...

⏱ بروزرسانی خودکار فعال شد
"""

async def main():
    bot = Bot(token=TOKEN)

    await bot.send_message(
        chat_id=CHANNEL,
        text=message
    )

    print("MESSAGE SENT")

if __name__ == "__main__":
    asyncio.run(main())
