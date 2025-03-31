from fastapi import FastAPI, File, UploadFile
from ultralytics import YOLO
from PIL import Image
import io
import numpy as np
import torch
from typing import List


app = FastAPI()

# setup
# device = "mps" if torch.backends.mps.is_available() else "cpu"
device = "cpu"
# model = YOLO("yolov8s-seg.pt")
model = YOLO("models/best.pt") 
model.to(device)


@app.get("/")
async def root():
    return {"message": "Food segmenter app"}


def segment_and_calculate_area(image_bytes):
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB") # convert the uploaded image file into a usable image
    results = model(image)[0] # results contain the masks, indexes and names

    response = []

    if results.masks is not None:
        # convert all masks from tensors to NumPy arrays
        masks = results.masks.data.cpu().numpy()

        class_ids = results.boxes.cls.cpu().numpy()

        for i, mask in enumerate(masks):
            area = int((mask > 0.5).sum())  # binary mask area (> 0.5 => True)
            class_name = model.names[int(class_ids[i])]
            response.append({
                "class": class_name,
                "area": area
            })

    return {"results": response}


@app.post("/segment")
async def segment_food(file: UploadFile = File(...)):
    contents = await file.read()
    result = segment_and_calculate_area(contents)
    return result


@app.post("/segment_batch")
async def segment_batch(files: List[UploadFile] = File(...)):
    all_results = []
    for file in files:
        contents = await file.read()
        result = segment_and_calculate_area(contents)
        all_results.append({
            "filename": file.filename,
            "results": result["results"]
        })
    return all_results
