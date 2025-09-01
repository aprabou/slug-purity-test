import sqlite3
import os
import tempfile
import shutil
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Lambda-compatible database setup
def get_db_path():
    # In Lambda, we need to use /tmp directory for writes
    if os.environ.get('AWS_LAMBDA_FUNCTION_NAME'):
        db_path = '/tmp/responses.db'
        # Copy initial DB from package if it doesn't exist
        if not os.path.exists(db_path):
            init_db_lambda(db_path)
        return db_path
    else:
        return 'responses.db'

DATABASE = get_db_path()

def init_db_lambda(db_path):
    """Initialize database for Lambda environment"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS question_stats (
                question_id INTEGER PRIMARY KEY,
                yes_count INTEGER DEFAULT 0
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS metadata (
                key TEXT PRIMARY KEY,
                value INTEGER DEFAULT 0
            )
        ''')
        
        # Initialize question stats (1-100)
        for i in range(1, 101):
            cursor.execute('INSERT OR IGNORE INTO question_stats (question_id, yes_count) VALUES (?, 0)', (i,))
        
        # Initialize total submissions counter
        cursor.execute('INSERT OR IGNORE INTO metadata (key, value) VALUES (?, ?)', ('total_submissions', 0))
        
        conn.commit()
        conn.close()
        print("Lambda database initialized successfully")
        return True
    except Exception as e:
        print(f"Lambda database initialization error: {e}")
        return False

def init_db():
    """Initialize database for local development"""
    if os.environ.get('AWS_LAMBDA_FUNCTION_NAME'):
        return True  # Skip for Lambda, handled in get_db_path()
    
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS question_stats (
                question_id INTEGER PRIMARY KEY,
                yes_count INTEGER DEFAULT 0
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS metadata (
                key TEXT PRIMARY KEY,
                value INTEGER DEFAULT 0
            )
        ''')
        
        # Initialize question stats (1-100)
        for i in range(1, 101):
            cursor.execute('INSERT OR IGNORE INTO question_stats (question_id, yes_count) VALUES (?, 0)', (i,))
        
        # Initialize total submissions counter
        cursor.execute('INSERT OR IGNORE INTO metadata (key, value) VALUES (?, ?)', ('total_submissions', 0))
        
        conn.commit()
        conn.close()
        print("Database initialized successfully")
        return True
    except Exception as e:
        print(f"Database initialization error: {e}")
        return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_responses():
    try:
        print("Form data received:", dict(request.form))
        
        # Get all checked questions
        checked_questions = []
        for key in request.form:
            if key.startswith('question') and request.form[key] == 'on':
                question_num = int(key.replace('question', ''))
                checked_questions.append(question_num)
                print(f"Question {question_num} was checked")
        
        print(f"Total checked questions: {len(checked_questions)}")
        
        # Update database
        db_path = get_db_path()
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Update question counts
        for question_id in checked_questions:
            cursor.execute('UPDATE question_stats SET yes_count = yes_count + 1 WHERE question_id = ?', 
                         (question_id,))
        
        # Increment total submissions
        cursor.execute('UPDATE metadata SET value = value + 1 WHERE key = ?', ('total_submissions',))
        
        conn.commit()
        conn.close()
        
        print("Database updated successfully")
        
        # Return success response for AJAX (no redirect)
        return {"status": "success"}, 200
    
    except Exception as e:
        print(f"Error processing submission: {e}")
        return {"status": "error", "message": str(e)}, 500

@app.route('/results')
def results():
    try:
        db_path = get_db_path()
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all question stats
        cursor.execute('SELECT question_id, yes_count FROM question_stats ORDER BY question_id')
        stats_data = cursor.fetchall()
        stats = {row[0]: row[1] for row in stats_data}
        
        # Get total submissions
        cursor.execute('SELECT value FROM metadata WHERE key = ?', ('total_submissions',))
        result = cursor.fetchone()
        total_submissions = result[0] if result else 0
        
        conn.close()
        
        return render_template('results.html', stats=stats, total_submissions=total_submissions)
    
    except Exception as e:
        print(f"Error getting results: {e}")
        return f"Error loading results: {e}", 500

@app.route('/api/results')
def api_results():
    try:
        db_path = get_db_path()
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all question stats
        cursor.execute('SELECT question_id, yes_count FROM question_stats ORDER BY question_id')
        stats_data = cursor.fetchall()
        stats = {str(row[0]): row[1] for row in stats_data}
        
        # Get total submissions
        cursor.execute('SELECT value FROM metadata WHERE key = ?', ('total_submissions',))
        result = cursor.fetchone()
        total_submissions = result[0] if result else 0
        
        conn.close()
        
        return jsonify({
            'total_submissions': total_submissions,
            'question_stats': stats,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        print(f"Error getting API results: {e}")
        return {"error": str(e)}, 500

# Initialize database when app starts (local development only)
if not os.environ.get('AWS_LAMBDA_FUNCTION_NAME'):
    init_db()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
