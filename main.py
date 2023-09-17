from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return jsonify({"message": "OK"})


@app.route("/predict", methods=["POST"])
def predict():
    return jsonify({"result": True})
