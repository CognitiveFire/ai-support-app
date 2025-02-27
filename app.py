import logging
import openai
import os
import time
import threading
import requests
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# ✅ Set up logging
LOG_FILE = "error.log"
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

print("🚀 Importing dependencies and setting up Flask app...")

# ✅ Initialize Flask App
app = Flask(__name__, static_folder="frontend/build", static_url_path="")
CORS(app)  # Allow cross-origin requests if needed

# ✅ Load OpenAI API Key from Railway environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    logging.error("❌ OpenAI API Key is missing! Set it in Railway.")
    raise ValueError("❌ Missing OpenAI API Key! Set it using environment variables.")

# ✅ Route to handle chat requests
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_prompt = data.get("prompt", "")

    if not user_prompt:
        return jsonify({"error": "❌ Missing prompt"}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Change to "gpt-3.5-turbo" if needed
            messages=[{"role": "user", "content": user_prompt}],
            max_tokens=1000
        )
        assistant_reply = response["choices"][0]["message"]["content"]
        return jsonify({"response": assistant_reply})

    except Exception as e:
        logging.error(f"❌ OpenAI API Error: {str(e)}")
        return jsonify({"error": f"❌ OpenAI API Error: {str(e)}"}), 500

# ✅ Serve the frontend
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    logging.info(f"Serving path: {path}")
    try:
        return send_from_directory(app.static_folder, "index.html")
    except Exception as e:
        logging.error(f"Error serving index.html: {str(e)}")
        return f"404: {str(e)}", 404

# ✅ Keep-Alive Function to Prevent Railway Shutdown
def keep_awake():
    railway_url = os.getenv("RAILWAY_URL")  # Use Railway’s public URL

    if not railway_url:
        print("⚠️ Warning: RAILWAY_URL is not set! Keep-alive may not work.")
        return

    while True:
        try:
            print(f"⏳ Sending keep-alive request to {railway_url}...")
            requests.get(railway_url)
        except requests.RequestException:
            print("⚠️ Keep-alive request failed!")
        time.sleep(600)  # Run every 10 minutes

# ✅ Run keep-alive in a separate background thread
threading.Thread(target=keep_awake, daemon=True).start()

# ✅ Run the Flask app
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    print(f"🚀 Starting Flask app on port {port}...")
    app.run(debug=True, host="0.0.0.0", port=port)
