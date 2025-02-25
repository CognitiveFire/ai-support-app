from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from openai import OpenAI
import os

# ✅ Initialize Flask App (Serve React Frontend)
app = Flask(__name__, static_folder="frontend/build", static_url_path="")
CORS(app)

# ✅ Debug: Check if API Key is Loaded
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    print("❌ ERROR: API key not found! Ensure it's set in Railway Variables.")
    raise ValueError("❌ Missing OpenAI API key! Set it using environment variables.")

print(f"✅ OpenAI API Key Loaded Successfully: {openai_api_key[:5]}... (hidden for security)")

# ✅ Initialize OpenAI Client with API Key
client = OpenAI(api_key=openai_api_key)

# ✅ Home Route - Serves React Frontend
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_react(path):
    """Serve React frontend from the build folder."""
    if path and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")

# ✅ Chat Route - Handles AI Requests
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        if not data or "message" not in data:
            return jsonify({"error": "❌ No message provided"}), 400

        user_input = data["message"]

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}]
        )

        assistant_reply = response.choices[0].message.content

        return jsonify({"response": assistant_reply})

    except Exception as e:
        return jsonify({"error": f"❌ OpenAI Error: {str(e)}"}), 500

# ✅ Run Flask App with Gunicorn Support
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))  # 👈 Use Railway's provided port (default: 8080)
    print(f"🚀 Starting Flask app on port {port}...")
    app.run(debug=True, host="0.0.0.0", port=port)
