import torch
from nanogpt.model import GPT
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder="frontend/build", static_url_path="/")
CORS(app, resources={r"/chat": {"origins": "https://chatbotinit-production.up.railway.app"}})

model_config = GPT.get_default_config()
model_config.model_type = None
model_config.vocab_size = 55  # From prepare.py
model_config.block_size = 64
model = GPT.from_pretrained(model_config, "out-n60ai/ckpt.pt")
model.eval()

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_react_app(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, "index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json(force=True)
        if not data or "prompt" not in data:
            return jsonify({"error": "Missing prompt"}), 400
        prompt = data["prompt"]
        input_ids = torch.tensor([ord(c) for c in prompt[:64] if ord(c) < 128], dtype=torch.long).unsqueeze(0)
        output = model.generate(input_ids, max_new_tokens=50, temperature=0.7)
        response = "".join(chr(i) for i in output[0].tolist() if 0 <= i <= 127)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": f"Error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.getenv("PORT", 8080)))