from flask import Flask, request
import requests
import os

app = Flask(__name__)

VERIFY_TOKEN = "seguro_token"  # el mismo que pusiste en Meta
TOKEN = "EAAVgZChpSqzABPSfwBP52KoGjmZBLVby371oQtks8rIK3zfZCqo3V1dDZAg1qzrFtE7deOPgvSsckXtafUA79zBZCemVvrjDnZAzVp4G2L9SoOoKzo9pirWvrsBNpgXx9lGnKqbsMM1HDd0ZCZCxUj7bfHMZBoNNrGm0IyCmtoVWiV60ZAPBzcHZC5lZAYPpsluPfaXu1WonT84Kz0ZC48AHhPvDBrZCRqFYUUzk10QzUnqhmROgbGrAZDZD"  # tu token de acceso largo
PHONE_NUMBER_ID = "704695322736553"  # tu ID de número

# Webhook
@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        return "Token inválido", 403

    elif request.method == "POST":
        data = request.get_json()
        print(data)  # 👀 Ver en logs lo que llega de WhatsApp

        # Verificamos si alguien mandó un mensaje
        if data and "messages" in data["entry"][0]["changes"][0]["value"]:
            mensaje = data["entry"][0]["changes"][0]["value"]["messages"][0]
            numero = mensaje["from"]   # Quien envió
            texto = mensaje["text"]["body"]  # Lo que escribió

            enviar_mensaje(numero, f"Recibí tu mensaje: {texto}")

        return "ok", 200


# Función para enviar mensajes
def enviar_mensaje(to, texto):
    url = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"
    headers = {"Authorization": f"Bearer {TOKEN}"}
    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": texto}
    }
    requests.post(url, headers=headers, json=data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))






