import streamlit as st
import sqlite3

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        st.error(f"Error connecting to database: {e}")
        return None

def create_users_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        conn.commit()
        st.success('Table "users" created successfully!')
    except sqlite3.Error as e:
        st.error(f"Error creating table: {e}")

def main():
    st.title('User Registration and Login')

    # Connect to the SQLite database
    conn = create_connection('users.db')

    # Check if connection is successful
    if conn is not None:
        st.success('Connected to the SQLite database successfully!')
    else:
        st.error('Failed to connect to the SQLite database')
        return

    # Create users table if it doesn't exist
    create_users_table(conn)

    # Rest of your Streamlit app code goes here

if __name__ == '__main__':
    main()
