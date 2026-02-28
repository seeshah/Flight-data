"""
Live Translation App - Flask Backend

Provides a web interface for real-time speech transcription (via the
browser's Web Speech API) and translates the transcribed text using
the googletrans library.

Usage:
    pip install -r requirements.txt
    python app.py

Then open http://localhost:5000 in Chrome, Edge, or Safari.
"""

from flask import Flask, render_template, request, jsonify
from googletrans import Translator

app = Flask(__name__)
translator = Translator()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/translate", methods=["POST"])
def translate_text():
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "No text provided"}), 400

    text = data["text"]
    source = data.get("source", "en")
    target = data.get("target", "es")

    try:
        result = translator.translate(text, src=source, dest=target)
        return jsonify({
            "translated": result.text,
            "source_lang": result.src,
            "target_lang": result.dest,
        })
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
