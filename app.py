import logging
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from openai import OpenAI
import os

# ✅ Initialize Flask App
app = Flask(__name__, static_folder="frontend/build", static_url_path="")
CORS(app)

# ✅ Configure Logging
LOG_FILE = "error.log"
logging.basicConfig(filename=LOG_FILE, level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")

# ✅ Load API Key from Environment Variable
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    logging.error("❌ Missing OpenAI API key! Set it using environment variables.")
    raise ValueError("❌ Missing OpenAI API key! Set it using environment variables.")

# ✅ Initialize OpenAI Client with API Key
client = OpenAI(api_key=openai_api_key)

# ✅ Chat Route - Handles AI Requests
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

# ✅ Run Flask App
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))  # 👈 Use environment variable for Railway
    print(f"🚀 Starting Flask app on port {port}...")
    app.run(debug=True, host="0.0.0.0", port=port)
