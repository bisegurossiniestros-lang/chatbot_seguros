from flask import Flask, request, jsonify
import requests, os, json

app = Flask(__name__)

VERIFY_TOKEN = "seguro_token"                 # Debe coincidir con el que pusiste en Meta
TOKEN = "EAAVgZChpSqzABPSfwBP52KoGjmZBLVby371oQtks8rIK3zfZCqo3V1dDZAg1qzrFtE7deOPgvSsckXtafUA79zBZCemVvrjDnZAzVp4G2L9SoOoKzo9pirWvrsBNpgXx9lGnKqbsMM1HDd0ZCZCxUj7bfHMZBoNNrGm0IyCmtoVWiV60ZAPBzcHZC5lZAYPpsluPfaXu1WonT84Kz0ZC48AHhPvDBrZCRqFYUUzk10QzUnqhmROgbGrAZDZD"                      # Tu token largo (EA...)
PHONE_NUMBER_ID = "806974345822226"           # Tu Phone Number ID

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
    print("📤 Enviando:", data)
    print("📥 Respuesta de Meta:", response.status_code, response.text)

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        # Validación con Meta
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        return "Error de verificación", 403
    
    if request.method == "POST":
        data = request.get_json()
        print("📥 JSON recibido:", data)   # 👈 aquí verás el mensaje en Render

        try:
            mensajes = data["entry"][0]["changes"][0]["value"].get("messages")
            if mensajes:
                texto = mensajes[0]["text"]["body"]
                de = mensajes[0]["from"]

                print(f"📲 Mensaje de {de}: {texto}")

                # Respuesta básica
                if "seguro" in texto.lower():
                    enviar_mensaje(de, "¡Claro! Te cuento sobre nuestros seguros 🚗🏠👨‍👩‍👧‍👦")
                else:
                    enviar_mensaje(de, "Gracias por escribirnos 🙌, ¿quieres información sobre seguros?")
        except Exception as e:
            print("⚠️ Error procesando el mensaje:", e)

        return "EVENT_RECEIVED", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
