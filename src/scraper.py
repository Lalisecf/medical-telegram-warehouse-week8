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
import json
from datetime import datetime
from pathlib import Path

# Load environment variables
load_dotenv()

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
PHONE = os.getenv("PHONE")

# Create Telegram client
client = TelegramClient("telegram_session", API_ID, API_HASH)

async def main():
    await client.start(phone=PHONE)

    channel = "CheMed123"   # Replace with the real channel username

    print(f"Reading messages from {channel}...")

    # Store all messages here
    messages = []

    async for message in client.iter_messages(channel, limit=20):

    # Download image if the message has a photo
     if message.photo:
        image_folder = Path(f"data/raw/images/{channel}")
        image_folder.mkdir(parents=True, exist_ok=True)

        image_path = image_folder / f"{message.id}.jpg"

        await client.download_media(
            message,
            file=image_path
        )
    else:
        image_path = None

        messages.append({
            "message_id": message.id,
            "date": str(message.date),
            "text": message.text,
            "views": message.views,
            "forwards": message.forwards,
            "has_media": message.media is not None,
            "image_path": str(image_path) if image_path else None
        })

    # Today's date
    today = datetime.now().strftime("%Y-%m-%d")

    # Create folder automatically
    output_dir = Path(f"data/raw/telegram_messages/{today}")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save JSON
    output_file = output_dir / "CheMed.json"

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=4)

    print(f"Saved {len(messages)} messages to {output_file}")
    
with client:
    client.loop.run_until_complete(main())