import os
import psycopg2
from flask import Flask, jsonify
from flask_cors import CORS
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
CORS(app)

# DB Config
DB_HOST = os.getenv("POSTGRES_HOST", "database")
DB_NAME = os.getenv("POSTGRES_DB", "teamboard")
DB_USER = os.getenv("POSTGRES_USER", "user")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "password")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        port=DB_PORT,
        cursor_factory=RealDictCursor
    )

@app.route('/api/health')
def health():
    return jsonify({"status": "active"})

@app.route('/api/info')
def info():
    return jsonify({
        "service": "TeamBoard Backend API",
        "version": "1.0.0"
    })

@app.route('/api/team')
def get_team():
    try:
        conn = get_db_connection()
        cur = conn.cursor() 
        cur.execute('SELECT * FROM members')
        members = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(members)
    except Exception as e:
        print(f"Error fetching team: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
        
@app.route('/api/team/<int:id>')
def get_member(id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM members WHERE id = %s', (id,))
        member = cur.fetchone()
        cur.close()
        conn.close()
        
        if not member:
            return jsonify({"error": "Member not found"}), 404
        
        return jsonify(member)
    except Exception as e:
        print(f"Error fetching member: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
