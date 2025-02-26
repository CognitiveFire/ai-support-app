import logging
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__, static_folder="frontend/build", static_url_path="")
CORS(app)

LOG_FILE = "error.log"
logging.basicConfig(filename=LOG_FILE, level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")

openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    logging.error("❌ Missing OpenAI API key! Set it using environment variables.")
    raise ValueError("❌ Missing OpenAI API key! Set it using environment variables.")

client = OpenAI(api_key=openai_api_key)

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        if not data or "message" not in data:
            logging.error("❌ No message provided in request.")
            return jsonify({"error": "❌ No message provided"}), 400
        user_input = data["message"]
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}]
        )
        assistant_reply = response.choices[0].message.content
        return jsonify({"response": assistant_reply})
    except Exception as e:
        logging.error(f"❌ OpenAI Error: {str(e)}")
        return jsonify({"error": f"❌ OpenAI Error: {str(e)}"}), 500

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    print(f"🚀 Starting Flask app on port {port}...")
    app.run(debug=True, host="0.0.0.0", port=port)
