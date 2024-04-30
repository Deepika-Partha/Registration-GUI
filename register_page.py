from tkinter import *
import tkinter as Register
from tkinter import ttk
from tkinter.tix import *
import sqlite3
import re
import string
from PIL import Image, ImageTk
from cryptography.fernet import Fernet

def signIn():
    register_window.destroy()
    import sign_in_page

def register():
    name = name_entry.get()
    lname = lastname_entry.get()
    month = months_myCombo.get()
    day = date_myCombo.get()
    year = year_entry.get()
    username = new_username_entry.get()
    password = pass_entry.get()
    cpass = confirm_pass_entry.get()
    dob = f"{month} {day} {year}"

    a = check_username(username)
    b = checkName(name)
    c = checkLastName(lname)
    d = checkDOB(month, day, year)
    e = check_password(password)
    f = check_confirm_pass(cpass,password)

    retrieve_password(username)

    if (a and b and c and d and e and f):
        password = encrypt_password(username, password)

        conn = sqlite3.connect('users_database.db')
        c = conn.cursor()

        c.execute('INSERT INTO users_profiles VALUES (:username, :first_name, :last_name, :date_of_birth, :password)',
            {
                'username': username,
                'first_name': name, 
                'last_name': lname, 
                'date_of_birth': dob , 
                'password': password

            })
        conn.commit()
        conn.close()

def encrypt_password(username, password):
    encrypted_pw = cipher_suite.encrypt(password.encode())
    with open(password_file, 'a') as file:
        file.write(f'{username}:{encrypted_pw.decode()}\n')
    return encrypted_pw

def retrieve_password(service): 
    with open('users_passwords.txt', 'r') as file:
        for line in file:
            stored_service, stored_pw = line.strip().split(':')
            if stored_service == service:
                return cipher_suite.decrypt(stored_pw.encode()).decode()
    return "Password not found"


def checkName(name):
    non_alpha_pattern = re.compile(r'[^a-zA-Z]')
    if ((non_alpha_pattern.search(name)) or (name.strip() == '')):
            name_error_label = Label(register_window, text='* Invalid name', fg='White',
                  font='skia 10')
            name_error_label.place(x=330,y=155)
            name_entry.after(5000, name_error_label.destroy)
            return False
    else:
        return True
    
def checkLastName(lname):
    non_alpha_pattern = re.compile(r'[^a-zA-Z]')
    if ((non_alpha_pattern.search(lname)) or (lname.strip() == '')):
            lname_error_label = Label(register_window, text='* Invalid last name', fg='White',
                  font='skia 10')
            lname_error_label.place(x=315,y=205)
            lastname_entry.after(5000, lname_error_label.destroy)
            return False
    else:
        return True
    
def checkDOB(month, day, year):
      year_val = True
      date_val = True
      if year != '':
            year = int(year)
      else:
           year = 0
      day = int(day)
      if 1920 <= year <= 2006:
            if month in ['January', 'March', 'May', 'July', 'August', 'October', 'December']:
                  if 1 <= day <= 31:
                        return True
            elif month in ['April', 'June', 'September', 'November']:
                  if 1 <= day <= 30:
                        return True
                  else:
                       date_val = False
            elif month == 'February':
                  if (year % 4 == 0):
                        if 1 <= day <= 29:
                              return True
                        else:
                             date_val = False
                  elif(1 <= day <= 28):
                        return True
                  else:
                        date_val = False   
      else:
            year_val = False

      # Display corresponding error message
      if(year_val == False):
            birthyear_error_label = Label(register_window, text='* Age not approved', fg='White',
            font='skia 10')
            birthyear_error_label.place(x=340,y=260)
            year_entry.after(5000, birthyear_error_label.destroy)
      elif(date_val == False):
            birthdate_error_label = Label(register_window, text='* Invalid birthdate', fg='White',
            font='skia 10')
            birthdate_error_label.place(x=340,y=260)
            year_entry.after(5000, birthdate_error_label.destroy)

      
def check_username(username):
    special_characters_pattern = re.compile(r'[^a-zA-Z0-9._]')
    if (special_characters_pattern.search(username) or (username.strip() == '')):
        username_error_label = Label(register_window, text='* Invalid username', fg='White',
        font='skia 10')
        username_error_label.place(x=310,y=305)
        new_username_entry.after(5000, username_error_label.destroy)
        return False
    else:
        return True
    
def check_password(password):
    a = False
    b = False
    c = False

    # Check length requirements
    if (len(password)>=8):
      a = True

    # Check number requirements
    numbers = '1234567890'
    for char in password:
        if char in numbers:
            b = True

    # Check special character requirements
    special_characters = '!@#$%^&*-_+=|;:,.<>?~'
    for char in password:
        if char in special_characters:
            c = True  

    # Display corresponding error message
    if(a == False):
            pass_len_error_label = Label(register_window, text='* Password not long enough', fg='White',
            font='skia 10')
            pass_len_error_label.place(x=270,y=355)
            pass_entry.after(5000, pass_len_error_label.destroy)
    elif(b == False):
            pass_num_error_label = Label(register_window, text='* Password must contain a number', fg='White',
            font='skia 10')
            pass_num_error_label.place(x=250,y=355)
            pass_entry.after(5000, pass_num_error_label.destroy)
    elif(c == False):
            pass_char_error_label = Label(register_window, text='* Password must contain a\nspecial character', fg='White',
            font='skia 10')
            pass_char_error_label.place(x=270,y=355)
            pass_entry.after(5000, pass_char_error_label.destroy)
    return a and b and c

def check_confirm_pass(cpass, password):
     if(cpass == password):
          return True
     else:
          confirm_pass_error_label = Label(register_window, text= "* Passwords don't match", fg='White',
          font='skia 10')
          confirm_pass_error_label.place(x=285,y=415)
          confirm_pass_entry.after(5000, confirm_pass_error_label.destroy)
          return False
                        
def hover_username(e):
     global temp_username_label
     temp_username_label = Label(register_window, text='Numbers, periods, and underscores\nallowed', fg='White',
      font='skia 10')
     temp_username_label.place(x=40, y=300)

def non_hover_username(e):
      temp_username_label.destroy()

def hover_password(e):
     global pass_entry_label
     pass_entry_label = Label(register_window, text='Requirements: 8 characters minimum\natleast one special character\natleast one number', fg='White',
      font='skia 10')
     pass_entry_label.place(x=35, y=350)

def non_hover_password(e):
      pass_entry_label.destroy()

# ENCRYPTION PROCESS
key = Fernet.generate_key()
cipher_suite = Fernet(key)
password_file = 'users_passwords.txt'
     
global register_window
    # Generate registration window for the functions
register_window = Register.Tk()
register_window.geometry('450x500')
register_window.title('Create an account')

createAccount_label = Label(register_window, text='Create an account',
          font='skia 40')
createAccount_label.place(x=40, y=50) 

first_name_label = Label(register_window, text='Please enter your name: ', fg='Red',
          font='skia 15')
first_name_label.place(x=40, y=130) 

name_entry = Entry(register_window)
name_entry.config(font=('skia', 15))
name_entry.config(bg='White')
name_entry.config(fg='Black')
name_entry.config(width=15)
name_entry.place(x=250,y=130)

last_name_label = Label(register_window, text='Please enter your last name: ', fg='Red',
      font='skia 15')
last_name_label.place(x=40, y=180) 

lastname_entry = Entry(register_window)
lastname_entry.config(font=('skia', 15))
lastname_entry.config(bg='White')
lastname_entry.config(fg='Black')
lastname_entry.config(width=15)
lastname_entry.place(x=250,y=180)

DOB_label = Label(register_window, text='Please enter your date\nof birth: ', fg='Red',
      font='skia 15')
DOB_label.place(x=40, y=230) 

# combo box for D.O.B 
months = [ 
      "January", 
      "February", 
      "March", 
      "April", 
      "May", 
      "June", 
      "July",
      "August", 
      "September", 
      "October", 
      "November",
      "December" 
] 

months_myCombo = ttk.Combobox(register_window,value=months)
months_myCombo.current(0)
months_myCombo.bind('<<ComboboxSelected>>')
months_myCombo.place(x=250, y=230)
months_myCombo.config(width=6)

date = ['1','2','3','4','5','6','7','8','9','10','11',
      '12','13','14','15','16','17','18','19','20','21',
      '22','23','24','25','26','27','28','29','30','31'] 

date_myCombo = ttk.Combobox(register_window,value=date)
date_myCombo.current(0)
date_myCombo.bind('<<ComboboxSelected>>')
date_myCombo.place(x=335, y=230)
date_myCombo.config(width=2)

year_entry = Entry(register_window)
year_entry.config(font=('skia', 15))
year_entry.config(bg='White')
year_entry.config(fg='Black')
year_entry.config(width=4)
year_entry.place(x=385,y=230)

username_label = Label(register_window, text='Please enter a username: ', fg='Red',
      font='skia 15')
username_label.place(x=40, y=280) 

new_username_entry = Entry(register_window)
new_username_entry.config(font=('skia', 15))
new_username_entry.config(bg='White')
new_username_entry.config(fg='Black')
new_username_entry.config(width=15)
new_username_entry.place(x=250,y=280)

new_username_entry.bind('<Enter>', hover_username)
new_username_entry.bind('<Leave>', non_hover_username)

pass_label = Label(register_window, text='Please enter a password: ', fg='Red',
      font='skia 15')
pass_label.place(x=40, y=330) 

pass_entry = Entry(register_window)
pass_entry.config(font=('skia', 15))
pass_entry.config(bg='White')
pass_entry.config(fg='Black')
pass_entry.config(width=15)
pass_entry.place(x=250,y=330)

pass_entry.bind('<Enter>', hover_password)
pass_entry.bind('<Leave>', non_hover_password)

confirm_pass_label = Label(register_window, text='Please confirm password: ', fg='Red',
      font='skia 15')
confirm_pass_label.place(x=40, y=390) 

confirm_pass_entry = Entry(register_window)
confirm_pass_entry.config(font=('skia', 15))
confirm_pass_entry.config(bg='White')
confirm_pass_entry.config(fg='Black')
confirm_pass_entry.config(width=15)
confirm_pass_entry.place(x=250,y=390)

reg_to_signIn = Button(register_window, text='Register', font='skia 15', command=register)
reg_to_signIn.place(x=340,y=450)

reg_create = Button(register_window, text='Sign in', font='skia 15', command=signIn)
reg_create.place(x=255,y=450)

# # create table
# conn = sqlite3.connect('users_database.db')
# c = conn.cursor()

# c.execute('''CREATE TABLE users_profiles(
#           username text, 
#           first_name text,
#           last_name text,
#           date_of_birth text,
#           password text       
# )
# ''')
# conn.commit()
# conn.close()


register_window.mainloop()