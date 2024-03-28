import numpy as np
import pandas as pd
import yfinance as yf
from keras.models import load_model
import streamlit as st
import matplotlib.pyplot as plt
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

# Load the pre-trained model
model = load_model('C:\Python\Stock\Stock Predictions Model.keras')
st.header('Stock Prediction System')

# Streamlit UI
def main():
    # Connect to the SQLite database
    conn = create_connection('users.db')

    st.title('Stock Prediction System')

    # Authentication
    st.subheader('Login')
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')

    if st.button('Login'):
        if authenticate_user(conn, username, password):
            st.success('Login successful!')
            
            st.subheader('Predictions')
            stock = st.text_input('Enter Stock Symbol', 'TSLA')
            start = '2012-01-01'
            end = '2023-12-31'

            data = yf.download(stock, start ,end)

            st.subheader('Stock Data')
            st.write(data)

            data_train = pd.DataFrame(data.Close[0: int(len(data)*0.80)])
            data_test = pd.DataFrame(data.Close[int(len(data)*0.80): len(data)])

            from sklearn.preprocessing import MinMaxScaler
            scaler = MinMaxScaler(feature_range=(0,1))

            pas_100_days = data_train.tail(100)
            data_test =pd.concat([pas_100_days, data_test], ignore_index=True)
            data_test_scale = scaler.fit_transform(data_test)

            st.subheader('Price vs MA50')
            ma_50_days = data.Close.rolling(50).mean()
            fig1 =plt.figure(figsize=(8,6))
            plt.plot(ma_50_days, 'r')
            plt.plot(data.Close, 'g')
            plt.show()
            st.pyplot(fig1)

            st.subheader('Price vs MA50 vs MA100')
            ma_100_days = data.Close.rolling(100).mean()
            fig2 =plt.figure(figsize=(8,6))
            plt.plot(ma_50_days, 'r')
            plt.plot(ma_100_days, 'b')
            plt.plot(data.Close, 'g')
            plt.show()
            st.pyplot(fig2)

            st.subheader('Price vs MA100 vs MA200')
            ma_200_days = data.Close.rolling(200).mean()
            fig3 =plt.figure(figsize=(8,6))
            plt.plot(ma_100_days, 'r')
            plt.plot(ma_200_days, 'b')
            plt.plot(data.Close, 'g')
            plt.show()
            st.pyplot(fig3)

            x = []
            y = []

            for i in range(100, data_test_scale.shape[0]):
                x.append(data_test_scale[i-100:i])
                y.append(data_test_scale[i,0])

            x, y = np.array(x), np.array(y)

            predict = model.predict(x)

            scale = 1/scaler.scale_

            predict = predict * scale
            y = y * scale

            st.subheader('Orginal Price vs Predicted Price')
            fig4 =plt.figure(figsize=(8,6))
            plt.plot(predict, 'r', label='Original Price')
            plt.plot(y, 'g', label = 'Predicted Price')
            plt.xlabel('Time')
            plt.ylabel('Price')
            plt.show()
            st.pyplot(fig4)
        else:
            st.error('Invalid username or password')  

    # User registration
    st.subheader('Register')
    new_username = st.text_input('New Username')
    new_password = st.text_input('New Password', type='password')
    confirm_password = st.text_input('Confirm Password', type='password')
    if st.button('Register'):
        if new_password != confirm_password:
            st.error('Passwords do not match')
        else:
            if create_user(conn, new_username, new_password):
                st.success('Registration successful!')
            else:
                st.error('Failed to register user')

if __name__ == '__main__':
    main()
