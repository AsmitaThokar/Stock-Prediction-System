import streamlit as st
import sqlite3 

# Function to create a connection to the SQLite database
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY,
                            username TEXT NOT NULL UNIQUE,
                            password TEXT NOT NULL
                        )''')
        conn.commit()
        return conn
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn

# Function to create a new user in the database
def create_user(conn, username, password):
    try:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(e)
        return False

# Function to authenticate user
def authenticate_user(conn, username, password):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    return cursor.fetchone() is not None



# Streamlit UI
def main():
    st.title('Stock Prediction System')

    # Connect to the SQLite database
    conn = create_connection('users.db')

    # Check if connection is successful
  

    # Page selection (Registration or Login)
    page_options = ['Registration', 'Login']
    page = st.sidebar.radio('Select Page', page_options)

    # User registration
    if page == 'Registration':
        st.subheader('Register')
        username = st.text_input('Username')
        password = st.text_input('Password', type='password')
        confirm_password = st.text_input('Confirm Password', type='password')

        if st.button('Register'):
            # Validate input
            if username.strip() == '':
                st.error('Username cannot be empty')
            elif password.strip() == '':
                st.error('Password cannot be empty')
            elif password != confirm_password:
                st.error('Passwords do not match')
            else:
                # Check if username already exists
                if conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone() is not None:
                    st.error('Username already exists')
                else:
                    # Create user
                    if create_user(conn, username, password):
                        st.success('Registration successful!')
                    else:
                        st.error('Failed to register user')

    # User login
    elif page == 'Login':
        st.subheader('Login')
        username = st.text_input('Username')
        password = st.text_input('Password', type='password')

        if st.button('Login'):
            if authenticate_user(conn, username, password):
                st.success('Login successful!')
            else:
                st.error('Invalid username or password')  
        

if __name__ == '__main__':
    main()


                
