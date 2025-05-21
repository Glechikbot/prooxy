import os
import re
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

IG_COOKIE = os.getenv("IG_COOKIE")
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Cookie": IG_COOKIE
}

@app.route("/")
def index():
    return "Instagram proxy is alive!"

@app.route("/download_instagram", methods=["POST"])
def download_instagram():
    try:
        data = request.get_json()
        url = data.get("url")
        if not url:
            return jsonify({"error": "Missing 'url'"}), 400

        response = requests.get(url, headers=HEADERS)
        html = response.text

        match = re.search(r'"video_url":"([^"]+)"', html)
        if match:
            video_url = match.group(1).replace("\\u0026", "&").replace("\\", "")
            return jsonify({"url": video_url})

        print("==== HTML START ====")
        print(html[:1000])
        print("==== HTML END ====")

        return jsonify({"error": "Video not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500
