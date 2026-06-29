#1.Import libraries
import os
import json
from pathlib import Path

import psycopg2
from dotenv import load_dotenv

#2.Load .env
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

#3.Connect to PostgreSQL
conn = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)

cursor = conn.cursor()

print("Connected to PostgreSQL")

# Create schema
cursor.execute("""
CREATE SCHEMA IF NOT EXISTS raw;
""")

conn.commit()

print("Schema created.")

#Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS raw.telegram_messages (

    message_id BIGINT,

    channel_name TEXT,

    message_date TIMESTAMP,

    message_text TEXT,

    views INTEGER,

    forwards INTEGER,

    image_path TEXT,

    has_media BOOLEAN,
               
    PRIMARY KEY (message_id, channel_name)

);
""")

conn.commit()

print("Table created.")

# Read JSON files 
json_folder = Path("data/raw/telegram_messages")

json_files = json_folder.rglob("*.json")

# Read each JSON file
for file in json_files:

    try:
        print(f"Loading {file}")

        with open(file, "r", encoding="utf-8") as f:
            messages = json.load(f)
            # Insert every message
            for message in messages:

                cursor.execute(
                """
                INSERT INTO raw.telegram_messages
                (
                    message_id,
                    channel_name,
                    message_date,
                    message_text,
                    views,
                    forwards,
                    image_path,
                    has_media
                )
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                ON CONFLICT (message_id, channel_name) DO NOTHING;
                """,
                (
                    message["message_id"],
                    message["channel_name"],
                    message["message_date"],
                    message["message_text"],
                    message["views"],
                    message["forwards"],
                    message["image_path"],
                    message["has_media"]
                )
            )
    except Exception as e:
     print(f"Error loading {file}: {e}")        

#Commit
conn.commit()

print("All messages inserted successfully.")  
#Close connection
cursor.close()
conn.close()

print("Database connection closed.")