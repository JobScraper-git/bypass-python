from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/extract', methods=['POST'])
def extract_redirect():
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    try:
        r = requests.head(url, allow_redirects=False, timeout=10)
        redirect_url = r.headers.get("Location")

        if not redirect_url:
            r = requests.get(url, allow_redirects=False, stream=True, timeout=10)
            redirect_url = r.headers.get("Location")

        return jsonify({"redirect_url": redirect_url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
