
from flask import Flask, request, jsonify, render_template, send_file
import sqlite3
import csv
import os

app = Flask(__name__)
DB_FILE = 'wsr_data.db'

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS weekly_status (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                year TEXT,
                month TEXT,
                weekdays TEXT,
                etria TEXT,
                solutions TEXT
            )
        ''')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data', methods=['GET'])
def load_data():
    try:
        with sqlite3.connect(DB_FILE) as conn:
            rows = conn.execute("SELECT year, month, weekdays, etria, solutions FROM weekly_status").fetchall()
        return jsonify(rows)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/save', methods=['POST'])
def save_data():
    data = request.json.get('tableData', [])
    try:
        with sqlite3.connect(DB_FILE) as conn:
            conn.execute("DELETE FROM weekly_status")  # Clear old data
            conn.executemany("INSERT INTO weekly_status (year, month, weekdays, etria, solutions) VALUES (?, ?, ?, ?, ?)", data)
        return jsonify({'message': 'Data saved successfully to SQLite.'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download')
def download_csv():
    try:
        with sqlite3.connect(DB_FILE) as conn:
            rows = conn.execute("SELECT year, month, weekdays, etria, solutions FROM weekly_status").fetchall()
        csv_file = 'WeeklyStatusReport.csv'
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Year', 'Month', 'Week Days', 'Etria', 'Solutions'])
            writer.writerows(rows)
        return send_file(csv_file, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=8080)
