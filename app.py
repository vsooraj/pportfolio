from flask import Flask, send_from_directory
import os

app = Flask(__name__, static_url_path='', static_folder='.')

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    if os.path.exists(path):
        return send_from_directory('.', path)
    return "Not Found", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
