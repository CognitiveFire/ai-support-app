import logging
print("Importing Flask...")
from flask import Flask, request, jsonify, send_from_directory
print("Importing CORS...")
from flask_cors import CORS
print("Importing OpenAI...")
from openai import OpenAI
print("Importing os...")
import os

print("Setting up Flask app...")
app = Flask(__name__, static_folder="frontend/build", static_url_path="")
print("Applying CORS...")
CORS(app)

LOG_FILE = "error.log"
print("Configuring logging...")
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

print("Checking OpenAI API key...")
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    logging.error("❌ Missing OpenAI API key! Set it using environment variables.")
    raise ValueError("❌ Missing OpenAI API key! Set it using environment variables.")

print("Initializing OpenAI client...")
client = OpenAI(api_key=openai_api_key)
print("OpenAI client initialized.")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        logging.info(f"Received chat request: {data}")
        if not data or "message" not in data:
            logging.error("❌ No message provided in request.")
            return jsonify({"error": "❌ No message provided"}), 400
        user_input = data["message"]
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}]
        )
        assistant_reply = response.choices[0].message.content
        logging.info(f"OpenAI response: {assistant_reply}")
        return jsonify({"response": assistant_reply})
    except Exception as e:
        logging.error(f"❌ OpenAI Error: {str(e)}")
        return jsonify({"error": f"❌ OpenAI Error: {str(e)}"}), 500

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    logging.info(f"Serving path: {path}")
    try:
        return send_from_directory(app.static_folder, 'index.html')
    except Exception as e:
        logging.error(f"Error serving index.html: {str(e)}")
        return f"404: {str(e)}", 404

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    print(f"🚀 Starting Flask app on port {port}...")
    print("Calling app.run()...")
    app.run(debug=True, host="0.0.0.0", port=port)
    print("Flask app running.")