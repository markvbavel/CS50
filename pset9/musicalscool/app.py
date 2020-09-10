import os
import sqlite3

from flask import Flask, flash, jsonify, redirect, render_template, request, session, g
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, eur, get_user_id, connect_db, insert_user, insert_student, close_connection

# Configure application
app = Flask(__name__)

# Configure SqLite3 database
database = ("database.db")
conn = connect_db(database)
conn.row_factory = sqlite3.Row
cur = conn.cursor()


user_data = ("admin", generate_password_hash("admin"))
insert_user(conn, user_data)
student_tuple = ("Mark", "van", "Bavel", "01-01-2001", "Gilze", "Groen", "1234567890", "0987654321", "test@text.com", "mark@test.com", "1", "Sjef", "some note")
insert_student(conn, student_tuple)

cur.execute("SELECT * FROM students")
result = cur.fetchall()

for row in result:
    print("students: {}".format(row))

close_connection(conn)



# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
#app.jinja_env.filters["eur"] = eur

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Home route
@app.route("/")
@login_required
def index():
    """Show overview of all students in a table"""
    if request.method == "GET":
        return render_template("index.html")
    
    else:
        return redirect("/")


# Login route
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST
    if request.method == "POST":

        # Error checking
        if not request.form.get("username"):
            return apology("must provide username", 403)

        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username

        """rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))"""

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET
    else:
        return render_template("index.html")

# Logout route
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

# Register route
@app.route("/register")
def register():
    if request.method == "POST":
        user_id = get_user_id()

        print(user_id)
    
    else:
        return render_template("index.html")

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)

# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)



