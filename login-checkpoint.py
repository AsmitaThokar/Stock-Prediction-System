# accounts = {"Test" : "Test1", "Test2" : "Password"}

# username = input("Please enter your username: ")
# password = input("Please enter the password for " + username + ": ")

# if (accounts.get(username) == password):
#     print("Login Successful")
#     test = input(".") #This is just so the program doesn't shut down as soon as you get the username ans password
# else:
#     print("Login Failed")



import tkinter as tk
from tkinter import messagebox

def register():
    # Implement your registration logic here
    username = entry_username.get()
    password = entry_password.get()
    # Save the user data to a database or file

    messagebox.showinfo("Registration", f"User {username} registered successfully!")

def login():
    # Implement your login logic here
    username = entry_username.get()
    password = entry_password.get()
    # Check if the user exists in the database or file

    messagebox.showinfo("Login", f"Welcome back, {username}!")

# Create the main window
root = tk.Tk()
root.title("Login and Registration")

# Create widgets
label_username = tk.Label(root, text="Username:")
entry_username = tk.Entry(root)
label_password = tk.Label(root, text="Password:")
entry_password = tk.Entry(root, show="*")
button_register = tk.Button(root, text="Register", command=register)
button_login = tk.Button(root, text="Login", command=login)

# Layout widgets
label_username.pack()
entry_username.pack()
label_password.pack()
entry_password.pack()
button_register.pack()
button_login.pack()

root.mainloop()
