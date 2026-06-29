# 1. Import libraries

# 2. Load .env variables

# 3. Connect to Telegram

# 4. Create folders

# 5. Read messages

# 6. Download images

# 7. Save JSON

# 8. Write logs

# 9. Main function

from telethon import TelegramClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
PHONE = os.getenv("PHONE")

# Create Telegram client
client = TelegramClient("telegram_session", API_ID, API_HASH)

async def main():
    await client.start(phone=PHONE)

    channel = "CheMed123"   # Replace with the actual username

    print(f"Reading messages from {channel}...\n")

    count = 0

    async for message in client.iter_messages(channel, limit=20):
        print("----------------------------")
        print("Message ID :", message.id)
        print("Date       :", message.date)
        print("Text       :", message.text)
        print("Views      :", message.views)

        count += 1

    print(f"\nTotal messages read: {count}")
    
with client:
    client.loop.run_until_complete(main())