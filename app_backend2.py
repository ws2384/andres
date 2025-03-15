from flask import Flask, render_template, jsonify, request
import json

app = Flask(__name__)

# Load the dialogue JSON file
with open("Un paciente con dolores de cabeza y mareos.json", "r", encoding="utf-8") as file:
    dialogues = json.load(file)

current_index = 0  # Track conversation progress

# Route to render the index page (HTML)
@app.route("/")
def index():
    return render_template("index.html")  # Make sure 'index.html' is in the templates folder

# Route to get the next dialogue
@app.route("/get_response", methods=["GET", "POST"])
def get_response():
    global current_index

    if request.method == "GET":
        return jsonify({
            "speaker": "Paciente",
            "text": "Buenos días, doctor. Recientemente he tenido mareos y fuertes dolores de cabeza."
        })

    if request.method == "POST":
        if current_index < len(dialogues):
            response = dialogues[current_index]
            current_index += 1
            return jsonify(response)
        else:
            return jsonify({"message": "End of conversation."})

if __name__ == "__main__":
    app.run(debug=True)
