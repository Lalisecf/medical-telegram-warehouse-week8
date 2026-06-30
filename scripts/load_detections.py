import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

# ---------------------------------------------------
# Load Environment Variables
# ---------------------------------------------------

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# ---------------------------------------------------
# PostgreSQL Connection
# ---------------------------------------------------


DATABASE_URL = URL.create(
    drivername="postgresql+psycopg2",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=int(DB_PORT),
    database=DB_NAME,
)

print(DATABASE_URL)

engine = create_engine(DATABASE_URL)
print("DATABASE_URL =", DATABASE_URL)
print("DB_HOST =", repr(DB_HOST))
print("DB_PORT =", repr(DB_PORT))
print("DB_NAME =", repr(DB_NAME))
print("DB_USER =", repr(DB_USER))

engine = create_engine(DATABASE_URL)

# ---------------------------------------------------
# CSV Path
# ---------------------------------------------------

CSV_PATH = "data/processed/detections.csv"

# ---------------------------------------------------
# Read CSV
# ---------------------------------------------------

print("Reading detection CSV...")

df = pd.read_csv(CSV_PATH)

print(df.head())

print(f"\nLoaded {len(df)} rows.")

# ---------------------------------------------------
# Create Schema
# ---------------------------------------------------

with engine.begin() as conn:

    conn.execute(text("""

        CREATE SCHEMA IF NOT EXISTS raw;

    """))

# ---------------------------------------------------
# Create Table
# ---------------------------------------------------

with engine.begin() as conn:

    conn.execute(text("""

    CREATE TABLE IF NOT EXISTS raw.image_detections (

        id SERIAL PRIMARY KEY,

        message_id BIGINT,

        channel_name TEXT,

        detected_class TEXT,

        confidence_score FLOAT,

        image_category TEXT

    );

    """))

print("Table ready.")

# ---------------------------------------------------
# Clear Previous Data
# ---------------------------------------------------

with engine.begin() as conn:

    conn.execute(text("""

    TRUNCATE TABLE raw.image_detections;

    """))

print("Previous rows removed.")

# ---------------------------------------------------
# Load Data
# ---------------------------------------------------

df.to_sql(

    name="image_detections",

    con=engine,

    schema="raw",

    if_exists="append",

    index=False,

    method="multi"

)

print("--------------------------------------")
print("YOLO detections loaded successfully!")
print("--------------------------------------")