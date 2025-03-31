import os
import cv2
import numpy as np
from tqdm import tqdm
from PIL import Image
import shutil

IMAGE_DIR = "raw_data/img_dir/train"
MASK_DIR = "raw_data/ann_dir/train"
OUTPUT_DIR = "yolo_data"
SPLIT = "train"

os.makedirs(f"{OUTPUT_DIR}/images/{SPLIT}", exist_ok=True)
os.makedirs(f"{OUTPUT_DIR}/labels/{SPLIT}", exist_ok=True)

def convert_mask_to_yolo(mask_path, label_path):
    mask = cv2.imread(mask_path, cv2.IMREAD_UNCHANGED)

    # unique object class IDs in mask (ignore background 0)
    class_ids = np.unique(mask)
    class_ids = class_ids[class_ids != 0]

    h, w = mask.shape[:2]
    with open(label_path, "w") as f:
        for class_id in class_ids:
            binary_mask = (mask == class_id).astype(np.uint8)

            # Find contours
            contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for contour in contours:
                if contour.shape[0] < 6:
                    continue  # ignore tiny regions

                # Normalize points
                points = contour.squeeze().astype(float)
                points[:, 0] /= w
                points[:, 1] /= h
                points = points.reshape(-1)

                # YOLO format: class_id x1 y1 x2 y2 ...
                points_str = " ".join([f"{p:.6f}" for p in points])
                f.write(f"{int(class_id - 1)} {points_str}\n")  # class_id -1 to make 0-indexed

print("Converting in progress")

for fname in tqdm(os.listdir(IMAGE_DIR)):
    if not fname.lower().endswith((".jpg", ".png")):
        continue

    img_path = os.path.join(IMAGE_DIR, fname)
    mask_path = os.path.join(MASK_DIR, fname.replace(".jpg", ".png"))
    label_path = os.path.join(OUTPUT_DIR, "labels", SPLIT, fname.replace(".jpg", ".txt").replace(".png", ".txt"))
    out_img_path = os.path.join(OUTPUT_DIR, "images", SPLIT, fname)

    if not os.path.exists(mask_path):
        continue

    convert_mask_to_yolo(mask_path, label_path)
    shutil.copy(img_path, out_img_path)

print("Done")
