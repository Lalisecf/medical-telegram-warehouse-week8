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


def main():
    """
    Scan all downloaded Telegram images,
    run YOLOv8 object detection,
    and prepare detection records.
    """

    records = []

    # Loop through each Telegram channel folder
    for channel in IMAGE_ROOT.iterdir():

        if not channel.is_dir():
            continue

        print(f"\nScanning channel: {channel.name}")

        # Loop through every JPG image
        for image_file in tqdm(channel.glob("*.jpg")):

            message_id = image_file.stem
            channel_name = channel.name

            try:
                # Run YOLO detection
                results = model(image_file)

                objects = []
                scores = []

                # Extract detected objects
                for result in results:

                    for box in result.boxes:

                        cls = int(box.cls)
                        confidence = float(box.conf)

                        name = model.names[cls]

                        objects.append(name)
                        scores.append(confidence)

                # Classify image
                category = classify_image(objects)

                # Average confidence
                if scores:
                    avg_confidence = sum(scores) / len(scores)
                else:
                    avg_confidence = 0

                # Store record
                records.append({
                    "message_id": message_id,
                    "channel_name": channel_name,
                    "detected_class": ",".join(objects),
                    "confidence_score": round(avg_confidence, 3),
                    "image_category": category
                })

            except Exception as e:
                print(f"Error processing {image_file}: {e}")

    return records


if __name__ == "__main__":
    records = main()