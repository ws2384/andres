from flask import Flask, render_template, jsonify, request
import json

app = Flask(__name__)

# Load the dialogue data
with open('/Users/williamsavage/Desktop/Chino/2024/SP/FINAL/dialogues/Un paciente con dolores de cabeza y mareos.json', 'r', encoding='utf-8') as f:
    dialogues = json.load(f)

conversation_index = 0

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_response", methods=["POST"])
def get_response():
    global conversation_index

    if conversation_index < len(dialogues):
        dialogue = dialogues[conversation_index]  # Get the current dialogue entry
        speaker_1 = dialogue.get("speaker_1", "...")
        text_1 = dialogue.get("text_1", "...")
        speaker_2 = dialogue.get("speaker_2", "...")
        text_2 = dialogue.get("text_2", "...")

        response = {
            "speaker_1": speaker_1,
            "text_1": text_1,
            "speaker_2": speaker_2,
            "text_2": text_2
        }

        conversation_index += 1  # Move to the next exchange
    else:
        response = {
            "speaker_1": "Fin",
            "text_1": "La conversación ha terminado. Refresca la página para reiniciar.",
            "speaker_2": "",
            "text_2": ""
        }

    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)
