from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Token y número que te da Meta
TOKEN = "PON_AQUI_TU_TOKEN"
PHONE_NUMBER_ID = "PON_AQUI_EL_ID_DEL_NUMERO"

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
        "type": "text",
        "text": {"body": texto}
    }
    requests.post(url, headers=headers, json=data)

# Webhook para recibir mensajes
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print("📩 Llego mensaje:", data)  # Para depuración

    if "messages" in data["entry"][0]["changes"][0]["value"]:
        mensaje = data["entry"][0]["changes"][0]["value"]["messages"][0]
        numero = mensaje["from"]
        texto = mensaje["text"]["body"].lower()

        # Respuestas según palabra clave
        if "auto" in texto:
            enviar_mensaje(numero, "🚗 Tenemos seguros de auto con cobertura total. ¿Quieres cotizar?")
        elif "vida" in texto:
            enviar_mensaje(numero, "❤️ Seguros de vida personalizados. ¿Quieres más información?")
        elif "salud" in texto:
            enviar_mensaje(numero, "🏥 Seguros de salud disponibles. ¿Quieres detalles?")
        else:
            enviar_mensaje(numero, "👋 Hola, ¿qué tipo de seguro buscas? (auto, vida, salud)")

    return jsonify({"status": "ok"})

# Para que WhatsApp valide el webhook
@app.route("/webhook", methods=["GET"])
def verificar():
    verify_token = "seguro_token"  # Cambia por tu token real
    if request.args.get("hub.verify_token") == verify_token:
        return request.args.get("hub.challenge")
    return "Error de verificación", 403

# Inicia la app (solo si se ejecuta local)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


