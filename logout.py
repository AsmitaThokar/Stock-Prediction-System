import streamlit as st

# Define valid credentials
VALID_USERNAME = "user"
VALID_PASSWORD = "password"

# Define a function to authenticate users
def authenticate(username, password):
    return username == VALID_USERNAME and password == VALID_PASSWORD

# Define a login page
def login():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if authenticate(username, password):
            st.success("Logged in successfully!")
            return True
        else:
            st.error("Invalid username or password")
            return False

# Define a logout button
def logout():
    if st.button("Logout"):
        session_state.authenticated = False

# Define a Streamlit SessionState class to keep track of user sessions
class SessionState:
    def __init__(self, **kwargs):
        self.username = None
        self.authenticated = False
        self.__dict__.update(kwargs)

# Main function to control app flow
def main():
    global session_state
    session_state = SessionState()
    
    if not session_state.authenticated:
        if not login():
            return
    
    st.title("Simple Number Calculator")
    
    # Add a logout button
    logout()
    
    # Input number from the user
    number = st.number_input("Enter a number", step=1)
    
    # Calculate square and cube
    square = number ** 2
    cube = number ** 3
    
    # Display results
    st.write(f"Square of {number} is: {square}")
    st.write(f"Cube of {number} is: {cube}")

if __name__ == "__main__":
    main()
