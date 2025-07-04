from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")  # This is pinged by UptimeRobot or similar

@app.route('/extract', methods=['POST'])
def extract_redirect():
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        )
    }

    try:
        # Follow redirects and get final URL
        r = requests.get(url, headers=headers, allow_redirects=True, timeout=15)
        final_url = r.url
        return jsonify({"redirect_url": final_url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
