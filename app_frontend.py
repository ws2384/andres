<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Simulación de Diálogo Médico</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            margin: 20px;
        }
        #chat-box {
            width: 60%;
            margin: auto;
            padding: 20px;
            border-radius: 10px;
            background-color: #f8f8f8;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
            text-align: left;
            max-height: 400px;
            overflow-y: auto;
        }
        .message {
            padding: 8px;
            margin: 5px 0;
            border-radius: 5px;
        }
        .doctor {
            background-color: #d1e7dd;
            text-align: right;
        }
        .patient {
            background-color: #f8d7da;
            text-align: left;
        }
        #input-box {
            display: flex;
            justify-content: center;
            align-items: center;
            margin-top: 10px;
        }
        input {
            width: 70%;
            padding: 10px;
            font-size: 16px;
            margin-right: 10px;
        }
        button {
            padding: 10px 15px;
            font-size: 16px;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <h1>Simulación de Diálogo Médico</h1>
    <div id="chat-box"></div>
    <div id="input-box">
        <input type="text" id="userInput" placeholder="Escribe tu respuesta...">
        <button onclick="submitResponse()">Enviar</button>
    </div>

    <script>
        let currentIndex = 0;
        let isDoctorTurn = false; // Track if it's the doctor's turn

        function fetchNextMessage() {
            fetch("/get_response", { method: "POST" })
                .then(response => response.json())
                .then(data => {
                    if (data.speaker && data.text) {
                        let chatBox = document.getElementById("chat-box");

                        // Append new message
                        let messageElement = document.createElement("p");
                        messageElement.classList.add("message", data.speaker === "Doctor" ? "doctor" : "patient");
                        messageElement.innerHTML = `<strong>${data.speaker}:</strong> ${data.text}`;
                        chatBox.appendChild(messageElement);
                        chatBox.scrollTop = chatBox.scrollHeight; // Auto-scroll

                        isDoctorTurn = (data.speaker === "Paciente"); // Doctor responds after patient

                        if (isDoctorTurn) {
                            document.getElementById("userInput").disabled = false;
                            document.getElementById("userInput").focus();
                        }
                    } else {
                        let endMessage = document.createElement("p");
                        endMessage.innerText = "Fin de la conversación.";
                        document.getElementById("chat-box").appendChild(endMessage);
                        document.getElementById("input-box").style.display = "none";
                    }
                })
                .catch(error => console.error("Error:", error));
        }

        function submitResponse() {
            let userInput = document.getElementById("userInput").value.trim();
            if (userInput !== "" && isDoctorTurn) {
                let chatBox = document.getElementById("chat-box");

                // Add the doctor's response
                let doctorMessage = document.createElement("p");
                doctorMessage.classList.add("message", "doctor");
                doctorMessage.innerHTML = `<strong>Doctor:</strong> ${userInput}`;
                chatBox.appendChild(doctorMessage);
                chatBox.scrollTop = chatBox.scrollHeight;

                document.getElementById("userInput").value = "";
                isDoctorTurn = false;

                setTimeout(fetchNextMessage, 1000); // Fetch next patient response
            }
        }

        // Start conversation with the first patient message
        fetchNextMessage();
    </script>
</body>
</html>
