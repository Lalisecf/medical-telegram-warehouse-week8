from ultralytics import YOLO
from pathlib import Path
import pandas as pd
from tqdm import tqdm

# Load YOLOv8 model
model = YOLO("yolov8n.pt")

# Input and output folders
IMAGE_ROOT = Path("data/raw/images")
OUTPUT = Path("data/processed")

# Create output directory
OUTPUT.mkdir(parents=True, exist_ok=True)

CSV_FILE = OUTPUT / "detections.csv"

# Objects considered as products
PRODUCT_OBJECTS = {
    "bottle",
    "cup",
    "vase",
    "wine glass"
}

def classify_image(objects):
    """
    Classify an image based on the detected objects.
    """

    has_person = "person" in objects
    has_product = any(obj in PRODUCT_OBJECTS for obj in objects)

    if has_person and has_product:
        return "promotional"

    elif has_product:
        return "product_display"

    elif has_person:
        return "lifestyle"

    return "other"