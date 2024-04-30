from tkinter import *
import tkinter as tk
import tkinter as signIn
import tkinter as Register
from tkinter import ttk
import sqlite3
import re
from PIL import Image, ImageTk
from cryptography.fernet import Fernet

# Generate Sign in window for the functions
signIn_window = signIn.Tk()
signIn_window.geometry('400x400')
signIn_window.title('Sign In')

#globals
username_space_errormsg = None
username_specialchars_errormsg = None

# Logo for Sign in
logo = ImageTk.PhotoImage(Image.open('registrationLogo.jpeg').resize((100,100)))
logoLabel = Label(signIn_window, image = logo)
logoLabel.place(x=145,y=50)

def register():
    signIn_window.destroy()
    import register_page

def signIn_submit_btn():
    username_entered = username_entry.get()
    password = password_entry.get()
    x = check_signin_username(username_entered)
    y = check_pass(password)
    print(retrieve_password(username_entered,password))
    # conn = sqlite3.connect('users_database.db')
    # c = conn.cursor()

    # c.execute('SELECT username FROM users_profiles')
    # records = c.fetchall()
    # print(records)

    # #commit changes
    # conn.commit()
    # #close connection
    # conn.close()
    
def check_signin_username(username):
    conn = sqlite3.connect('users_database.db')
    c = conn.cursor()
    string_user = username 
    c.execute('SELECT username FROM users_profiles WHERE username=?', (string_user,))
    checkUsername = c.fetchone()
    
    special_characters_pattern = re.compile(r'[^a-zA-Z0-9._]')
    if (special_characters_pattern.search(username) or (username.strip() == '')):
        username_error_label = Label(signIn_window, text='Invalid username', fg='Red',
        font='skia 13')
        username_error_label.place(x=190,y=265)
        username_entry.after(5000, username_error_label.destroy)
        return False
    elif checkUsername is None:
        # print('check:',checkUsername)
        # print('username:',string_user)
        print('Username does not exist')
    else:
        return True

def check_pass(password):
    conn = sqlite3.connect('users_database.db')
    c = conn.cursor()
    c.execute('SELECT password FROM users_profiles WHERE password=?', (password,))
    checkPassword = c.fetchone()
    # if checkPassword is None:
    #     print('Password is incorrect')
    # else:
    #     print('Logged In!')

def retrieve_password(service, password): 
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)
    password_file = 'users_passwords.txt'

    with open(password_file, 'r') as file:
        for line in file:
            stored_service, stored_pw = line.strip().split(':')
            if stored_service == service:
                print(stored_service)
                print(stored_pw)
                # temp = bytes(stored_pw, "utf-8")
                # print(temp)
                # f = Fernet(temp)
                message = str.encode(password)
                encrypted_message = cipher_suite.decrypt(message)
                real_pass = encrypted_message.decode()
                return real_pass
    return "Password not found"

def click(event):
   username_entry.configure(state=NORMAL)
   username_entry.delete(0, END)
   username_entry.unbind('<Button-1>', clicked)

def click2(event):
   password_entry.configure(state=NORMAL)
   password_entry.delete(0, END)
   password_entry.unbind('<Button-1>', clicked2)

# ENCRYPTION PROCESS
key = Fernet.generate_key()
cipher_suite = Fernet(key)
password_file = 'users_passwords.txt'

# Sign in Entries and Labels
signIn_label = Label(signIn_window, text='Sign In',
          font='skia 40')
signIn_label.place(x=135, y=175)

global username_entry
username_entry = Entry(signIn_window)
username_entry.config(font=('skia', 15))
username_entry.config(bg='White')
username_entry.config(fg='Black')
username_entry.insert(0,' Please enter username')
username_entry.config(width=17)
username_entry.place(x=115,y=240)
clicked = username_entry.bind('<Button-1>', click)

global password_entry
password_entry = Entry(signIn_window)
password_entry.config(font=('skia', 15))
password_entry.config(bg='White')
password_entry.config(fg='Black')
password_entry.insert(0,' Please enter password')
password_entry.config(width=17)
password_entry.place(x=115,y=290)
clicked2 = password_entry.bind('<Button-1>', click2)

# Button for  Sign in
signIn_register = Button(signIn_window, text='Register', font='skia 15', command=register)
signIn_register.place(x=210,y=350)

signIn_submit = Button(signIn_window, text='Sign in', font='skia 15', command=signIn_submit_btn)
signIn_submit.place(x=300,y=350)


signIn_window.mainloop()
