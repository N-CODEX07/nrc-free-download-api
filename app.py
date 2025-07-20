from flask import Flask, request, jsonify, send_file
import yt_dlp
import os
import uuid
import requests

app = Flask(__name__)
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# --- YOUTUBE DOWNLOAD ---
@app.route('/api/youtube', methods=['POST'])
def download_youtube():
    data = request.json
    url = data.get("url")
    quality = data.get("quality", "best")  # example: 360, 720, 1080, or "best"

    if not url:
        return jsonify({"error": "Missing YouTube URL"}), 400

    try:
        filename = f"{uuid.uuid4()}.mp4"
        filepath = os.path.join(DOWNLOAD_DIR, filename)

        ydl_opts = {
            'outtmpl': filepath,
            'format': f'bestvideo[height<={quality}]+bestaudio/best' if quality.isdigit() else quality,
            'merge_output_format': 'mp4'
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return send_file(filepath, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- INSTAGRAM DOWNLOAD ---
@app.route('/api/instagram', methods=['POST'])
def download_instagram():
    data = request.json
    url = data.get("url")

    if not url:
        return jsonify({"error": "Missing Instagram URL"}), 400

    try:
        filename = f"{uuid.uuid4()}.mp4"
        filepath = os.path.join(DOWNLOAD_DIR, filename)

        ydl_opts = {
            'outtmpl': filepath,
            'merge_output_format': 'mp4',
            'format': 'best'
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return send_file(filepath, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- HOME ---
@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "message": "Welcome to the YouTube + Instagram Downloader API",
        "endpoints": {
            "/api/youtube": "POST {url, quality}",
            "/api/instagram": "POST {url}"
        }
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
