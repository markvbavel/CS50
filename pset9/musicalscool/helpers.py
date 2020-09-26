import os
import requests
import urllib.parse

import sqlite3
from flask import redirect, render_template, request, session
from functools import wraps
 

def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def connect_db(db_file):
    """ Returns SQLite3 connection """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("Succesfully connected to {}".format(db_file))    
        return conn
    except sqlite3.Error as error:
        print("Failed to connect to database. Error:", error)


def close_connection(conn):
    """ Closes connection to SQLite3 database """
    if conn:
        try:
            conn.close()
        except sqlite3.Error as error:
            print("Failed to close connection. Error: ", error)
        else:
            print("SQLite connection is closed.")


def dict_factory(cursor, row):
    """ Returns dictionary """
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d    


def get_headers(conn):
    """
    returns headers for database
    """
    try:
        cur = conn.cursor()
        headers = []
        cur.execute("PRAGMA table_info(students)")
    except sqlite3.Error as error:
        print("Pragma failed. Error: ", error)
    else:
        for col in cur.fetchall():
            headers.append(col["name"])
        print("Pragma succeeded")
        return headers
        

def insert_user(conn, user_data):
    """
    user_data = username, hash
    
    Returns user_id of user inserted
    """
    try:
        sql = "INSERT INTO users (username, hash) VALUES (?, ?)"
        cur = conn.cursor()
        cur.execute(sql, user_data)
    except sqlite3.Error as error:
        print("Failed to insert user into users table. Error:", error)
        conn.rollback()
    else:
        conn.commit()    
        print(cur.rowcount, "record(s) inserted successfully into users table.")
        return cur.lastrowid


def insert_student(conn, student_data):
    """
    student_data = Firstname, Lastname, Birthdate, Class, Phone, Phone2, Email, Email2, Cast, Role, Notes
    
    Returns student_id of student inserted
    """
    try:
        sql = """INSERT INTO students 
                (Firstname, Lastname, Birthdate, Class, Phone, Phone2, Email, Email2, Cast, Role, Notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
        cur = conn.cursor()
        cur.execute(sql, student_data)
    except sqlite3.Error as error:
        print("Failed to insert student data into students table. Error:", error)  
        conn.rollback()  
    else:
        conn.commit()
        print(cur.rowcount, "record(s) inserted succesfully into students table.")
        return cur.lastrowid

def search_user(conn, username):
    """Returns list of users matching the username""" 
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username =?",(username,))
    except sqlite3.Error as error:
        print("Failed to search user table. Error: ", error)
    else:
        records = cur.fetchall() 
        print(len(records),"record(s) matched the search query on users table.")
        if records == None:
            return 0
        else:
            return records   

def student_overview(conn):
    """ Returns all students in database """
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM students")
        records = cur.fetchall()
    except sqlite3.Error as error:
        print("Failed to display student overview. Error: ", error)
    else:
        if len(records) >= 1:
            print(len(records),"record(s) found in students table.")
            return records

def search_student(conn, query, column):
    """Returns list of students"""
    try:
        cur = conn.cursor()
        headers = get_headers(conn)
        if column in headers:
            cur.execute("SELECT * FROM students WHERE "+column+" LIKE ?",('%'+query+'%',))
            records = cur.fetchall()
    except sqlite3.Error as error:
        print("Failed to search students table. Error: ", error)
    else:
        if len(records) >= 1:
            print(len(records),"record(s) matched the search query on students table.")
            return records
  

def mod_user(conn, user_data, user_id):
    """ 
    user_data = username, hash, id

    Returns user id that was modified 
    """
    (username, pw_hash) = user_data
    try:
        cur = conn.cursor()
        records = cur.execute("UPDATE users SET username=?, hash=? WHERE id=?", (username, pw_hash, user_id))
    except sqlite3.Error as error:
        print("Failed to update user data. Error: ", error)
        conn.rollback()
    else:
        conn.commit()
        print("user", user_id,"was succesfully updated.")
        return records


def del_entry(conn, entry_id):
    """ Deletes student entry from database """

    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM students WHERE id =?", (entry_id,))
    except sqlite3.Error as error:
        print("Failed to delete student data. Error: ", error)
        conn.rollback()
    else:
        conn.commit()
        print("Student entry ", entry_id, "deleted.")
        return


def del_user(conn, user_id):
    """ Deletes user from database """
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM users WHERE id =?", (user_id,))
    except sqlite3.Error as error:
        print("Failed to delete user data. Error: ", error)
        conn.rollback()
    else:
        conn.commit()
        print("User", user_id,"deleted from database.")
        return
