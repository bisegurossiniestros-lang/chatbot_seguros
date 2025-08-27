from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# 👇 Usa tu token largo de Meta y el ID del número de WhatsApp
TOKEN = "EAAVgZChpSqzABPVZBcy4ZBKDm8ZCY4Vb0wMjDeK0M15ZB16mDgRH363DkDYgCSQZBZBpb7hlCH0QI0XUunRjfmf2j1PhflZArMr9Nl9EIWq3QQkljzTM5Xg1yYaQoEHBWPIZCyL5Tsor0g6RZB42d5mZA8WIOYDmi7ZAAZAEx9LxcmUZAnupkeZBLc38wKc4ZAlO0sYuAqs2W7yCHaTEZCfWQncL1ZAeAZCJCm1y6vEJYYTHoSTfZClotbnuAZAkZD"
PHONE_NUMBER_ID = "806974345822226"

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




