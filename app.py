from flask import Flask, request, jsonify
import requests, os, json

app = Flask(__name__)

VERIFY_TOKEN = "seguro_token"                 # Debe coincidir con el que pusiste en Meta
TOKEN = "EAAVgZChpSqzABPSfwBP52KoGjmZBLVby371oQtks8rIK3zfZCqo3V1dDZAg1qzrFtE7deOPgvSsckXtafUA79zBZCemVvrjDnZAzVp4G2L9SoOoKzo9pirWvrsBNpgXx9lGnKqbsMM1HDd0ZCZCxUj7bfHMZBoNNrGm0IyCmtoVWiV60ZAPBzcHZC5lZAYPpsluPfaXu1WonT84Kz0ZC48AHhPvDBrZCRqFYUUzk10QzUnqhmROgbGrAZDZD"                      # Tu token largo (EA...)
PHONE_NUMBER_ID = "806974345822226"           # Tu Phone Number ID

@app.route("/", methods=["GET"])
def ok():
    return "Bot de seguros activo ✅", 200

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if mode == "subscribe" and token == VERIFY_TOKEN:
            return challenge, 200
        return "Token inválido", 403

    # POST: mensaje entrante
    data = request.get_json(silent=True)
    print("📥 Evento recibido:\n", json.dumps(data, ensure_ascii=False, indent=2))

    try:
        value = data["entry"][0]["changes"][0]["value"]
        # Solo procesamos si hay mensajes (ignora 'statuses' u otros eventos)
        if "messages" in value:
            msg = value["messages"][0]
            from_num = msg["from"]  # ej: "51987654321"
            if msg.get("type") == "text":
                text = msg["text"]["body"].strip().lower()
            else:
                text = ""

            # Reglas simples de respuesta
            if "auto" in text:
                reply = "🚗 Seguro de auto con cobertura total. ¿Quieres cotizar?"
            elif "vida" in text:
                reply = "❤️ Seguro de vida personalizado. ¿Te cuento opciones?"
            elif "salud" in text:
                reply = "🏥 Seguro de salud disponible. ¿Qué plan te interesa?"
            elif text:
                reply = f"👋 Recibí: “{text}”. Escribe: auto, vida o salud."
            else:
                reply = "👋 Hola, ¿qué tipo de seguro buscas? (auto, vida, salud)"

            enviar_mensaje(from_num, reply)
    except Exception as e:
        print("⚠️ Error procesando:", e)

    return jsonify({"status": "ok"}), 200

def enviar_mensaje(to, body):
    url = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": body}
    }
    r = requests.post(url, headers=headers, json=payload)
    print("📤 Respuesta de Meta:", r.status_code, r.text)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
