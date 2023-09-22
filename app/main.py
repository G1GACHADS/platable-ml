import io
import json

import torch
import torchvision.transforms as transforms
from flask import Flask, Response, jsonify, request
from PIL import Image
from ultralytics import YOLO

app = Flask(__name__)

MODEL_PATH = "app/best.pt"


def get_prediction(img):
    model = YOLO(MODEL_PATH)
    results = model.predict(img)
    result = results[0]
    output = []
    for box in result.boxes:
        x1, y1, x2, y2 = [round(x) for x in box.xyxy[0].tolist()]
        class_id = box.cls[0].item()
        prob = round(box.conf[0].item(), 2)
        output.append([x1, y1, x2, y2, result.names[class_id], prob])
    return output


@app.route("/", methods=["GET"])
def root():
    return jsonify({"message": "OK"}), 200


@app.route("/demo", methods=["GET"])
def demo():
    with open("app/index.html") as f:
        return f.read()


ALLOWED_EXTENSIONS = ("png", "jpg", "jpeg")


def file_is_allowed(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/predict", methods=["POST"])
def predict():
    file = request.files.get("image")
    if file is None or file.filename == "":
        return jsonify({"error": "no file"}), 422
    if not file_is_allowed(file.filename):
        return jsonify({"error": "file format not supported"}), 422

    try:
        img = Image.open(file.stream)
        results = get_prediction(img)

        response = []
        for result in results:
            response.append(
                {
                    "x1": result[0],
                    "y1": result[1],
                    "x2": result[2],
                    "y2": result[3],
                    "class": result[4],
                    "probability": result[5],
                }
            )

        return jsonify(response), 200
    except Exception as e:
        return jsonify({"result": e}), 500
