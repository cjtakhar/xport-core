
# db.py
import psycopg2
from psycopg2.extras import RealDictCursor
import logging

DATABASE_URL = "postgresql://kt:3535@localhost/xport"

def get_db_connection():
    try:
        conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
        logging.info("Database connection established")
        return conn
    except Exception as e:
        logging.error("Database connection failed: %s", e)
        return None