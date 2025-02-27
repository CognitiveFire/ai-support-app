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
CORS(app)  # Allow cross-origin requests

# ✅ Load OpenAI API Key from Railway environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    logging.error("❌ OpenAI API key is missing! Make sure it's set in Railway.")
    raise ValueError("❌ OpenAI API key is missing! Set it in Railway.")

# ✅ Initialize OpenAI client
client = openai.OpenAI(api_key=openai_api_key)
print("✅ OpenAI client initialized.")

# ✅ Fetch `RAILWAY_URL`
railway_url = os.getenv("RAILWAY_URL")
print(f"🔍 Debug: RAILWAY_URL from environment: {railway_url}")

if not railway_url:
    logging.error("❌ RAILWAY_URL is not set! Keep-alive will not work.")

# ✅ Keep-Alive Function to Prevent Railway Shutdown
def keep_awake(railway_url):
    """Prevents Railway from shutting down the app."""
    if not railway_url:
        logging.error("❌ RAILWAY_URL is not set! Keep-alive will not work.")
        return

    while True:
        try:
            print(f"⏳ Sending keep-alive request to {railway_url}...")
            requests.get(railway_url)
        except requests.RequestException as e:
            print(f"⚠️ Keep-alive request failed! {str(e)}")
        time.sleep(600)  # Run every 10 minutes

# ✅ Start keep-alive function in the background
threading.Thread(target=keep_awake, args=(railway_url,), daemon=True).start()

# ✅ Define a test route to verify the API is running
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "🚀 ChatGPT API is running!"})

# ✅ Chatbot Endpoint
@app.route("/chat", methods=["POST"])
def chat():
    try:
        logging.info("🔹 Received a request at /chat")
        data = request.get_json()

        if not data or "prompt" not in data:
            logging.error("❌ No prompt received")
            return jsonify({"error": "Missing prompt"}), 400

        user_prompt = data["prompt"]
        logging.info(f"🔹 Processing request: {user_prompt}")

        response = client.chat.completions.create(
            model="gpt-4",  # Change to "gpt-3.5-turbo" if needed
            messages=[{"role": "user", "content": user_prompt}],
            max_tokens=1000
        )

        assistant_reply = response.choices[0].message.content
        logging.info(f"✅ OpenAI Response: {assistant_reply}")
        return jsonify({"response": assistant_reply})
    
    except Exception as e:
        logging.error(f"❌ Error in /chat: {str(e)}")
        return jsonify({"error": f"OpenAI API Error: {str(e)}"}), 500

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

# ✅ Run the Flask app
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    print(f"🚀 Starting Flask app on port {port}...")
    app.run(debug=True, host="0.0.0.0", port=port)
