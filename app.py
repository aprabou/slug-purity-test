import sqlite3
import os
from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Use environment variable for database path in production
DATABASE = os.environ.get('DATABASE_URL', 'responses.db')
# Handle PostgreSQL URLs if using Heroku Postgres
if DATABASE.startswith('postgres://'):
    DATABASE = DATABASE.replace('postgres://', 'postgresql://', 1)

def init_db():
    # For SQLite (simple deployment)
    if not DATABASE.startswith('postgresql://'):
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
        print("SQLite database initialized successfully")

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
        conn = sqlite3.connect(DATABASE)
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

@app.route('/admin/results')
def admin_results():
    conn = sqlite3.connect(DATABASE)
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
    
    print(f"Debug - Total submissions: {total_submissions}")
    print(f"Debug - Stats sample: {dict(list(stats.items())[:5])}")
    
    return render_template('results.html', stats=stats, total_submissions=total_submissions)

@app.route('/api/results')
def api_results():
    conn = sqlite3.connect(DATABASE)
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

if __name__ == '__main__':
    init_db()
    # Use environment variables for production
    port = int(os.environ.get('PORT', 3000))
    debug = os.environ.get('FLASK_ENV', 'development') == 'development'
    app.run(debug=debug, host='0.0.0.0', port=port)
