from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import json
import os

app = Flask(__name__, static_folder="static")  
CORS(app)

# Path to the JSON file (adjust if you move the file)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_DIR, os.getenv("DIALOGUE_JSON_PATH", "Unpacientecondoloresdecabezaymareos.json"))

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
        print(f"❌ Error loading dialogue: {e}")  # Logs error to Render console
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))  # Use Render's assigned port
    app.run(host="0.0.0.0", port=port)
