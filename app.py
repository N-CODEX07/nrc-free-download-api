from flask import Flask, request, jsonify, send_file
from yt_dlp import YoutubeDL
from io import BytesIO
import tempfile
import uuid

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Welcome to NRC YouTube + Instagram Downloader API (Vercel Fix)",
        "endpoints": {
            "/api/youtube": "POST {url, quality (optional)}",
            "/api/instagram": "POST {url}"
        }
    })

@app.route("/api/youtube", methods=["POST"])
def download_youtube():
    try:
        data = request.json
        url = data.get("url")
        quality = data.get("quality", "best")

        if not url:
            return jsonify({"error": "Missing URL"}), 400

        # Use temp file instead of disk saving
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")

        ydl_opts = {
            'outtmpl': temp_file.name,
            'format': f'bestvideo[height<={quality}]+bestaudio/best' if quality.isdigit() else quality,
            'merge_output_format': 'mp4',
            'quiet': True,
            'no_warnings': True
        }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return send_file(temp_file.name, mimetype="video/mp4", as_attachment=True,
                         download_name=f"{uuid.uuid4()}.mp4")

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/instagram", methods=["POST"])
def download_instagram():
    try:
        data = request.json
        url = data.get("url")

        if not url:
            return jsonify({"error": "Missing URL"}), 400

        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")

        ydl_opts = {
            'outtmpl': temp_file.name,
            'format': 'best',
            'merge_output_format': 'mp4',
            'quiet': True,
            'no_warnings': True
        }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return send_file(temp_file.name, mimetype="video/mp4", as_attachment=True,
                         download_name=f"{uuid.uuid4()}.mp4")

    except Exception as e:
        return jsonify({"error": str(e)}), 500
