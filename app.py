from flask import Flask, request
import requests, os, json, logging

app = Flask(__name__)

# Configurar logging
logging.basicConfig(level=logging.INFO)

# Configuración
VERIFY_TOKEN = "seguro_token"  # Asegúrate de usar este mismo token en el panel de Meta
TOKEN = "EAAVgZChpSqzABPW3PSukKbtxZAsdHXHUy6zZAHMO2qz0PMnnRuw9qYbBaqbZALMWaL0uW8A49SOfgR7ZBxni1h64FeT9DfwBZAqU1VDSw40zxffeahTZClTZADIa4a7ELP1FIyXlYuZBAnbOBYFsvBWAfPVXGGintZB5UgN4T3wVfP2qA4QQGnyoGWcTdCGNw0OtSuMt7SVc04jTn75ZBu0qpcG4iXe2WICpj3QW9NhtyJh9X2qUz98n1r9fQrXcrwjDNYZD"     # Tu token largo válido
PHONE_NUMBER_ID = "806974345822226"

# Función para enviar mensaje de WhatsApp
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
    logging.info("📤 Enviando mensaje a: %s", to)
    logging.info("📥 Respuesta Meta: %s %s", response.status_code, response.text)

# Ruta del Webhook
@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        token_enviado = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if token_enviado == VERIFY_TOKEN:
            return challenge, 200
        return "Error de verificación", 403

    if request.method == "POST":
        data = request.get_json(force=True, silent=True)

        if not data:
            logging.warning("⚠️ No se recibió ningún JSON.")
            return "NO_JSON", 400

        logging.info("📥 JSON recibido:")
        logging.info(json.dumps(data, indent=2))

        try:
            mensajes = (
                data.get("entry", [{}])[0]
                    .get("changes", [{}])[0]
                    .get("value", {})
                    .get("messages")
            )

            if not mensajes:
                mensajes = data.get("value", {}).get("messages")

            if mensajes:
                mensaje = mensajes[0]
                texto = mensaje.get("text", {}).get("body", "")
                de = mensaje.get("from")
                logging.info(f"📲 Mensaje de {de}: {texto}")

                if texto and "seguro" in texto.lower():
                    enviar_mensaje(de, "¡Claro! Te cuento sobre nuestros seguros 🚗🏠👨‍👩‍👧‍👦")
                else:
                    enviar_mensaje(de, "Gracias por escribirnos 🙌, ¿quieres información sobre seguros?")
            else:
                logging.warning("⚠️ No se encontraron mensajes válidos.")
        except Exception as e:
            logging.error("⚠️ Error procesando el mensaje: %s", e)

        return "EVENT_RECEIVED", 200

# Ejecutar servidor Flask
if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=PORT)



