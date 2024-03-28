import sqlite3
import hashlib

# Function to create a connection to the SQLite database
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
        return conn

# Function to create a new user in the database
def create_user(conn, username, password):
    try:
        cursor = conn.cursor()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(e)
        return False

# Function to authenticate user
def authenticate_user(conn, username, password):
    cursor = conn.cursor()
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, hashed_password))
    return cursor.fetchone() is not None
