from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# 👇 Usa tu token largo de Meta y el ID del número de WhatsApp
TOKEN = "EAAVgZChpSqzABPS5VCi710BYu9mzoBX3XsaxElxfsdK3zXykBcCoDG3GaCbDRczZBA1KvFeviEzhONnec6gjkrs4GvaueiTZAKiJeXiEsCZCHbhqd5HMsBSbs35vU3K2SiwjuZCVw4m7W77ceYd0pBEefmT6DDiDTiZCxjbuBsyjaBqh6AdRsxuhwGG6ZA8LCXijJCQYmH1odGOB2JdBdrWBcMyRX40Qt6uYG54IXZAmFVpeNgZDZD"
PHONE_NUMBER_ID = "704695322736553"

# Función para enviar mensajes
def enviar_mensaje(to, texto):
    url = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "text": {"body": texto}
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()

@app.route("/", methods=["GET"])
def verificar():
    return "Bot de seguros activo ✅"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)



