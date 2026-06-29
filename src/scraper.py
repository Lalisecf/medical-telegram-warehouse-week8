# 1. Import libraries

# 2. Load .env variables

# 3. Connect to Telegram

# 4. Create folders

# 5. Read messages

# 6. Download images

# 7. Save JSON

# 8. Write logs

# 9. Main function

# 1. Import libraries

from telethon import TelegramClient
from dotenv import load_dotenv
import os
import json
from datetime import datetime
from pathlib import Path
import logging

  # 7. Save JSON for this channel

logging.basicConfig(
        filename="logs/scraper.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

# 2. Load .env variables
load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
PHONE = os.getenv("PHONE")

# 3. Connect to Telegram
client = TelegramClient("telegram_session", API_ID, API_HASH)


async def main():

    await client.start(phone=PHONE)

    # 4. List of channels
    channels = [
        "CheMed123",          
        "Lobelia4Cosmetics",  
        "tikvahpharma"       
    ]

    # Today's date
    today = datetime.now().strftime("%Y-%m-%d")

    # Folder for JSON files
    output_dir = Path(f"data/raw/telegram_messages/{today}")
    output_dir.mkdir(parents=True, exist_ok=True)

   # 5. Loop through every channel
    for channel in channels:

        try:

            print(f"\nReading messages from {channel}...")
            logging.info(f"Reading messages from {channel}")

            messages = []

            # Read messages
            async for message in client.iter_messages(channel, limit=500):

                image_path = None

                # Download image if available
                if message.photo:

                    image_folder = Path(f"data/raw/images/{channel}")
                    image_folder.mkdir(parents=True, exist_ok=True)

                    image_path = image_folder / f"{message.id}.jpg"

                    await client.download_media(
                        message,
                        file=image_path
                    )

                # Save message information
                messages.append({
                    "message_id": message.id,
                    "channel_name": channel,
                    "message_date": str(message.date),
                    "message_text": message.text,
                    "views": message.views,
                    "forwards": message.forwards,
                    "has_media": message.media is not None,
                    "image_path": str(image_path) if image_path else None
                })

            # Save JSON
            output_file = output_dir / f"{channel}.json"

            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(messages, f, ensure_ascii=False, indent=4)

            print(f"Saved {len(messages)} messages to {output_file}")
            logging.info(f"Saved {len(messages)} messages for {channel}")

        except Exception as e:

            print(f"Error scraping {channel}: {e}")
            logging.error(f"Error scraping {channel}: {e}")

            continue


# Run the scraper
with client:
    client.loop.run_until_complete(main())