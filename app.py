from flask import Flask, send_from_directory, request, jsonify
import os
import sqlite3

app = Flask(__name__, static_url_path='', static_folder='.')

def init_db():
    conn = sqlite3.connect('portfolio.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL,
            subject TEXT NOT NULL,
            message TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Initialize DB on startup
init_db()

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api/contacts/', methods=['GET', 'POST'])
def handle_contacts():
    if request.method == 'POST':
        data = request.json
        conn = sqlite3.connect('portfolio.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO contacts (first_name, last_name, email, subject, message)
            VALUES (?, ?, ?, ?, ?)
        ''', (data.get('first_name'), data.get('last_name'), data.get('email'), data.get('subject'), data.get('message')))
        conn.commit()
        conn.close()
        return jsonify({"message": "Success"}), 201
    else:
        conn = sqlite3.connect('portfolio.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute('SELECT * FROM contacts ORDER BY id DESC')
        rows = c.fetchall()
        conn.close()
        return jsonify([dict(row) for row in rows]), 200

@app.route('/<path:path>')
def serve_static(path):
    if os.path.exists(path):
        return send_from_directory('.', path)
    return "Not Found", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
