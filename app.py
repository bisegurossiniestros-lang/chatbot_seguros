from flask import Flask, request, jsonify
import requests, os, json

app = Flask(__name__)

VERIFY_TOKEN = "seguro_token"                 # Debe coincidir con el que pusiste en Meta
TOKEN = "EAAVgZChpSqzABPSfwBP52KoGjmZBLVby371oQtks8rIK3zfZCqo3V1dDZAg1qzrFtE7deOPgvSsckXtafUA79zBZCemVvrjDnZAzVp4G2L9SoOoKzo9pirWvrsBNpgXx9lGnKqbsMM1HDd0ZCZCxUj7bfHMZBoNNrGm0IyCmtoVWiV60ZAPBzcHZC5lZAYPpsluPfaXu1WonT84Kz0ZC48AHhPvDBrZCRqFYUUzk10QzUnqhmROgbGrAZDZD"                      # Tu token largo (EA...)
PHONE_NUMBER_ID = "806974345822226"           # Tu Phone Number ID

# Función para enviar un mensaje de texto
def enviar_mensaje(to, texto):
    url = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": texto}
    }
    requests.post(url, headers=headers, json=data)

# Ruta webhook
@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        # Validación de Meta
        verify_token = "seguro_token"
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if mode == "subscribe" and token == verify_token:
            return challenge, 200
        return "Error de validación", 403

    if request.method == "POST":
        data = request.get_json()
        print("📥 Evento recibido:", data)

        try:
            mensajes = data["entry"][0]["changes"][0]["value"].get("messages")
            if mensajes:
                mensaje = mensajes[0]
                texto = mensaje["text"]["body"]
                de = mensaje["from"]

                # 👉 Aquí pones tu lógica
                if "seguro" in texto.lower():
                    enviar_mensaje(de, "Claro, tenemos seguros disponibles. ¿Quieres que te muestre opciones?")
                else:
                    enviar_mensaje(de, f"Recibí tu mensaje: {texto}")

        except Exception as e:
            print("❌ Error procesando mensaje:", e)

        return "EVENT_RECEIVED", 200

    app.run(host="0.0.0.0", port=port)

