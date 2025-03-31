from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import json
import os

app = Flask(__name__, static_folder="static")  
CORS(app)

# Define the path to the dialogue JSON file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_DIR, os.getenv("DIALOGUE_JSON_PATH", "dialogues/Unpacientecondoloresdecabezaymareos.json"))

@app.route("/")
def serve_index():
    return send_from_directory("static", "index.html")

@app.route("/get_dialogue")
def get_dialogue():
    try:
        with open(JSON_PATH, "r", encoding="utf-8") as file:
            data = json.load(file)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ != "__main__":
    # This ensures that the app runs properly with Gunicorn on Render
    gunicorn_app = app
