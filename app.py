import sqlite3
from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# AWS Lambda requires us to write to the /tmp folder
# If running locally, this file will just appear in your temp folder
DB_PATH = "C:\\Users\\skoch\\LEAP-LIFE\\leap-life-sam\\game_database.db"


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_name TEXT NOT NULL,
            score INTEGER NOT NULL
        )
        ''')


# Initialize the DB immediately when the app loads
initialize_database()


@app.route('/')
def game():
    current_high_score = 0
    champion_name = "CPU"

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT player_name, score FROM Scores ORDER BY score DESC LIMIT 1")
            row = cursor.fetchone()
            if row:
                champion_name = row['player_name']
                current_high_score = row['score']
    except Exception as e:
        print(f"Database error: {e}")

    return render_template('game.html', high_score=current_high_score, champion=champion_name)


@app.route('/submit_score', methods=['POST'])
def submit_score():
    data = request.get_json()
    name = data.get('name', 'Anonymous')
    score = data.get('score', 0)

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Scores (player_name, score) VALUES (?, ?)", (name, score))
            conn.commit()
    except Exception as e:
        print(f"Error saving score: {e}")
        return jsonify({'status': 'error'}), 500

    return jsonify({'status': 'success'})


if __name__ == '__main__':
    app.run(debug=True)
