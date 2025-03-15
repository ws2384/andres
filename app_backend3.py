from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import json
import os

app = Flask(__name__, static_folder="static")  # Serve static files from the 'static' folder
CORS(app)

# Serve the HTML page when visiting "/"
@app.route("/")
def serve_index():
    return send_from_directory("static", "index.html")  # Serve the HTML file

# Serve the JSON dialogue data
@app.route("/get_dialogue")
def get_dialogue():
    json_path = "/Users/williamsavage/Desktop/Chino/2024/SP/FINAL/dialogues/Un paciente con dolores de cabeza y mareos.json"
    with open(json_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
