import os
from telegram import Bot

TOKEN = os.environ["BOT_TOKEN"]
CHANNEL = os.environ["CHANNEL_ID"]

bot = Bot(token=TOKEN)

message = """
📊 گزارش تست بازار

🟡 طلا: در حال دریافت...
₿ بیت‌کوین: در حال دریافت...

⏱ بروزرسانی خودکار فعال شد
"""

bot.send_message(
    chat_id=CHANNEL,
    text=message
)

print("Message sent successfully")
