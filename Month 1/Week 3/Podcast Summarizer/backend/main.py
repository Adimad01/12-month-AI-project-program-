from flask import Flask, request, jsonify
from flask_cors import CORS
import whisper
import tempfile
import os
import requests

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])  # Autorise React

whisper_model = whisper.load_model("base")  # ou "medium", "large"
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "mistral"

def summarize_with_ollama(transcript):
    response = requests.post(OLLAMA_URL, json={
        "model": OLLAMA_MODEL,
        "prompt": f"Summarize this podcast transcript:\n\n{transcript[:4000]}",
        "stream": False
    })
    return response.json().get("response", "No summary generated.")

@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        path = tmp.name
        file.save(path)

    try:
        result = whisper_model.transcribe(path)
        transcript = result["text"]
        summary = summarize_with_ollama(transcript)

        quotes = [s.strip() for s in transcript.split(".") if len(s.strip()) > 50][:5]

        return jsonify({
            "summary": summary,
            "quotes": quotes
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        os.remove(path)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
