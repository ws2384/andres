from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = Flask(__name__, static_folder="static")  
CORS(app)

# Get dialogue JSON path from .env
JSON_PATH = os.getenv("DIALOGUE_JSON_PATH")

@app.route("/")
def serve_index():
    return send_from_directory("static", "index.html")

@app.route("/get_dialogue")
def get_dialogue():
    if not JSON_PATH:
        return jsonify({"error": "JSON file path is not set"}), 500
    
    try:
        with open(JSON_PATH, "r", encoding="utf-8") as file:
            data = json.load(file)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
