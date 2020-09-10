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


def eur(value):
    """Format value as eur."""
    return f"${value:,.2f}"


def get_user_id():
    """Gets user ID"""
    user_id = session["user_id"]
    return user_id


def connect_db(db_file):
    """Returns SQLite3 connection"""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("Succesfully connected to {}".format(db_file))    
        return conn

    except sqlite3.Error as error:
        print("Failed to connect to database. Error:", error)

def dict_factory(cursor, row):
    """ Returns dictionary """
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d    

def insert_user(conn, user_data):
    """Returns user id"""

    try:
        sql = "INSERT INTO users (username, hash) VALUES (?, ?)"

        cur = conn.cursor()
        cur.execute(sql, user_data)
    except sqlite3.Error as error:
        print("Failed to insert user into users table. Error:", error)
        conn.rollback()
    else:
        conn.commit()    
        print(cur.rowcount, "records inserted successfully into users table.")
    finally:
        return cur.lastrowid


def insert_student(conn, student_data):
    """Returns student id"""

    try:
        sql = """INSERT INTO students 
                (first, middle, last, birth, city, class, tel_1, tel_2, email_1, email_2, cast, role, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
        cur = conn.cursor()
        cur.execute(sql, student_data)
    except sqlite3.Error as error:
        print("Failed to insert student data into students table. Error:", error)  
        conn.rollback()  
    else:
        conn.commit()
        print(cur.rowcount, "records inserted succesfully into students table.")
    finally:
        return cur.lastrowid

def close_connection(conn):
    """ Closes connection to SQLite3 database """
    if conn:
        conn.close()
        print("SQLite connection is closed.")