# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_db_connection
import logging

app = Flask(__name__)
CORS(app)

@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    # Hash the password
    hashed_password = generate_password_hash(password)

    conn = get_db_connection()
    if conn is None:
        return jsonify({'success': False, 'message': 'Database connection failed'}), 500

    cur = conn.cursor()
    try:
        # Check if user already exists
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        if cur.fetchone() is not None:
            return jsonify({'success': False, 'message': 'Email already in use'}), 409

        # Insert new user
        cur.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, hashed_password))
        conn.commit()
        return jsonify({'success': True, 'message': 'User created successfully'}), 201

    except Exception as e:
        logging.error("Error executing query: %s", e)
        return jsonify({'success': False, 'message': 'Error executing query'}), 500
    finally:
        cur.close()
        conn.close()

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    conn = get_db_connection()
    if conn is None:
        return jsonify({'success': False, 'message': 'Database connection failed'}), 500

    cur = conn.cursor()
    try:
        cur.execute("SELECT id, email, password FROM users WHERE email = %s", (email,))
        user = cur.fetchone()

        if user and check_password_hash(user['password'], password):
            logging.info("User authenticated successfully")
            return jsonify({'success': True, 'message': 'Login successful'}), 200
        else:
            return jsonify({'success': False, 'message': 'Invalid email or password'}), 401

    except Exception as e:
        logging.error("Error executing query: %s", e)
        return jsonify({'success': False, 'message': 'Error executing query'}), 500
    finally:
        cur.close()
        conn.close()

@app.route('/')
def home():
    return "Welcome to xport!"

if __name__ == '__main__':
    app.run(debug=True)
