from flask import request, jsonify
from paddleocr import PaddleOCR
from tensorflow.keras.models import load_model
import numpy as np
import os

ocr = PaddleOCR(lang="en")
model_path = "./model/nutrition_model.h5"
model = load_model(model_path)

def process_ocr():
    file = request.files["image"]
    image_path = f"./uploads/{file.filename}"
    file.save(image_path)

    results = ocr.ocr(image_path, cls=True)
    text = "\n".join([line[1][0] for line in results[0]])

    return jsonify({"text": text})