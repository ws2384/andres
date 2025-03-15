<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Diálogo Médico</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f4f4f4;
        }
        .dialogue-container {
            max-width: 720px; 
            height: 600px; /* Same height */
            margin: auto;
            padding: 20px;
            border-radius: 10px;
            background-color: #fff;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
            overflow-y: auto;
            position: relative;
        }
        .message {
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 10px;
            max-width: 70%; /* Each message takes up less space */
            word-wrap: break-word;
            border: 2px solid transparent;
        }
        .doctor {
            background-color: #d1e7fd;
            border-color: #007bff;
            text-align: left;
            align-self: flex-end;
        }
        .andres {
            background-color: #d4edda;
            border-color: #28a745;
            text-align: left;
            align-self: flex-start;
        }
        .hint {
            background-color: #e2d5f7;
            border-color: #6a0dad;
            text-align: right;
            font-style: italic;
            max-width: 70%;
            align-self: flex-end;
        }
        .patient {
            background-color: #fdd1d1;
            border-color: #dc3545;
            text-align: right;
            align-self: flex-end;
        }
        .user {
            background-color: #e6e6e6;
            text-align: right;
            font-style: italic;
            align-self: flex-end;
        }
        .input-container {
            display: none;
            margin-top: 20px;
            display: flex;
            gap: 10px;
        }
        input {
            flex: 1;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
        button {
            padding: 10px 15px;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        button:disabled {
            background-color: #ccc;
            cursor: not-allowed;
        }
        .mic-button {
            background-color: #28a745;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            color: white;
            cursor: pointer;
        }
        .title {
            text-align: center;
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 20px;
        }
        .instructions {
            text-align: center;
            font-size: 18px;
            margin-bottom: 20px;
            font-style: italic;
        }
        #dialogue-box {
            display: flex;
            flex-direction: column;
        }
    </style>
</head>
<body>

    <div class="title">Un paciente con dolores de cabeza y mareos</div>
    <div class="instructions">Hace clic en "Siguiente" para iniciar la conversación con tu paciente, Andres. Usa el teclado o tu voz (usando el botón 🎤) para responder después de cada "Hint".</div>

    <div class="dialogue-container" id="dialogue-container">
        <div id="dialogue-box"></div>
        <button id="next-btn" onclick="showNext()">Siguiente</button>
        <div class="input-container" id="input-container">
            <input type="text" id="user-input" placeholder="Escribe tu respuesta...">
            <button class="mic-button" onclick="startSpeechRecognition()">🎤</button>
            <button id="send-btn" onclick="sendResponse()">Enviar</button>
        </div>
    </div>

    <script>
        let dialogue = [];
        let index = 0;

        async function fetchDialogue() {
            try {
                const response = await fetch("http://127.0.0.1:5000/get_dialogue");
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                dialogue = await response.json();
            } catch (error) {
                console.error("Error fetching dialogue:", error);
            }
        }

        function displayMessage(messageObj) {
            const dialogueBox = document.getElementById("dialogue-box");
            const messageDiv = document.createElement("div");
            messageDiv.classList.add("message");

            const speakerLower = messageObj.speaker.toLowerCase();
            if (speakerLower === "doctor") {
                messageDiv.classList.add("doctor");
            } else if (speakerLower === "andres") {
                messageDiv.classList.add("andres");
            } else if (speakerLower === "hint") {
                messageDiv.classList.add("hint");
            } else if (speakerLower === "paciente") {
                messageDiv.classList.add("patient");
            } else {
                messageDiv.classList.add("user");
            }

            messageDiv.textContent = `${messageObj.speaker}: ${messageObj.text}`;
            dialogueBox.appendChild(messageDiv);
            scrollToBottom();
        }

        function scrollToBottom() {
            const dialogueContainer = document.getElementById("dialogue-container");
            dialogueContainer.scrollTop = dialogueContainer.scrollHeight;
        }

        function showNext() {
            if (index === 0) {
                // Start the dialogue once the user clicks 'Siguiente'
                fetchDialogue().then(() => {
                    if (dialogue.length > 0) {
                        displayMessage(dialogue[index]);
                        index++;
                        document.getElementById("input-container").style.display = "flex";
                        document.getElementById("next-btn").disabled = false; // Ensure it's enabled
                    }
                });
            } else if (index < dialogue.length) {
                displayMessage(dialogue[index]);
                index++;

                // If the speaker is "Hint", disable the button
                if (dialogue[index - 1].speaker.toLowerCase() === "hint") {
                    document.getElementById("next-btn").disabled = true;
                } else {
                    document.getElementById("next-btn").disabled = false;
                }

                document.getElementById("input-container").style.display = "flex";
            }

            if (index >= dialogue.length) {
                document.getElementById("next-btn").disabled = true;
            }
        }

        function sendResponse() {
            const userInput = document.getElementById("user-input");
            const userText = userInput.value.trim();
            
            if (userText === "" || index >= dialogue.length) return;

            displayMessage({ speaker: "Tú", text: userText });

            userInput.value = "";
            document.getElementById("input-container").style.display = "none";

            setTimeout(() => {
                if (index < dialogue.length) {
                    displayMessage(dialogue[index]);
                    index++;
                    document.getElementById("next-btn").disabled = false;
                }
                if (index >= dialogue.length) {
                    document.getElementById("next-btn").disabled = true;
                }
            }, 1000);
        }

        function startSpeechRecognition() {
            if (!('webkitSpeechRecognition' in window)) {
                alert("Tu navegador no soporta reconocimiento de voz.");
                return;
            }

            const recognition = new webkitSpeechRecognition();
            recognition.lang = "es-ES";
            recognition.continuous = false;
            recognition.interimResults = false;

            recognition.onresult = function(event) {
                document.getElementById("user-input").value = event.results[0][0].transcript;
            };

            recognition.onerror = function(event) {
                console.error("Error en reconocimiento de voz:", event.error);
            };

            recognition.start();
        }
    </script>

</body>
</html>
