import os
import re
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

IG_COOKIE = os.getenv("IG_COOKIE", "")
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Cookie": IG_COOKIE
}

@app.route("/")
def index():
    return "Instagram proxy is alive!", 200

@app.route("/download_instagram", methods=["POST"])
def download_instagram():
    data = request.get_json(silent=True)
    insta_url = data.get("url") if data else None
    if not insta_url:
        return jsonify({"error": "Missing 'url' in request"}), 400

    resp = requests.get(insta_url, headers=HEADERS, timeout=10)
    html = resp.text

    match = re.search(r'"video_url":"([^"]+)"', html)
    if match:
        # Використовуємо правильну екранціію backslash
        video_url = match.group(1).replace("\\\\u0026", "&").replace("\\\\", "")
        return jsonify({"url": video_url})

    print("==== HTML START ====")
    print(html[:1000])
    print("==== HTML END ====")

    return jsonify({"error": "Video not found"}), 404

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)