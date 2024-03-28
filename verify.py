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

    # Rest of your Streamlit app code goes here

if __name__ == '__main__':
    main()
