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
    print("Connecting to Telegram...")
    await client.start(phone=PHONE)
    print("Connected successfully!")

with client:
    client.loop.run_until_complete(main())