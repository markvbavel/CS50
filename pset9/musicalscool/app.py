import os
import sqlite3
import secrets  

from flask import Flask, flash, jsonify, redirect, render_template, request, session, g
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, eur, get_user_id, connect_db, close_connection, dict_factory
from helpers import insert_student, insert_user, search_user, search_student, mod_student, mod_user


# Configure application
app = Flask(__name__)


# Configure SqLite3 database
database = ("database.db")

"""# Add admin to database.db
conn = connect_db(database)
conn.row_factory = dict_factory
cur = conn.cursor()

password = generate_password_hash("admin")
print(password)
cur.execute("INSERT INTO users (username, hash) VALUES (?, ?)", ("admin", password))
conn.commit()

records = cur.execute("SELECT * FROM users").fetchall()
for row in records:
    print("row: ", row)"""



# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = "xSuNYjNGBBEpHzSUapYIuVXmc-ROL2zDcVvkbPLDfVY"
Session(app)


# Home route
@app.route("/")
def index():
    """Show overview of all students in a table"""
    if request.method == "POST":

        """TODO"""

        # Close database connection 
        # close_connection(conn)

        return redirect("/")    

    else:
        return render_template("index.html", session = Session)



# Login route
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # User reached route via POST
    if request.method == "POST":

        # Connect to database 
        conn = connect_db(database)
        conn.row_factory = dict_factory

        # Gather form input
        username = request.form.get("login_username")
        password = generate_password_hash(request.form.get("login_password"))

        # Error checking on user input
        if not username or not password:
            return apology("Please fill in all the required fields", 403)

        # Query users table for username
        records = search_user(conn, username)

        # Ensure username exists and password is correct
        if len(records) != 1:
            return apology("username not found", 403)
        elif check_password_hash(records[0]["hash"], password) == False:
            return apology("Invalid password", 403)
                        
        # Remember which user has logged in
        session["user_id"] = records[0]["id"]
        session["USERNAME"] = records[0]["username"]

        print("session user_id: ", session["user_id"])
        print("session username: ", session["USERNAME"])

        # Close database connection
        close_connection(conn)

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

    # Close database connection
    # close_connection(conn)

    # Redirect user to login form
    return redirect("/")

# Register route
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        # Clear current user id
        session.clear()

        # Connect to database 
        conn = connect_db(database)
        conn.row_factory = dict_factory

        # Get username and password from form
        username = request.form.get("register_username")
        password = generate_password_hash(request.form.get("register_password"))
        confirm = generate_password_hash(request.form.get("register_confirm"))
        
        # Error check
        records = search_user(conn, username)
        print("records: ", records)

    
        #   If user is in database
        #   if passwords do not match
        #   if all input fields are provided
            


        # Insert username and password into database

        # Close database connection
        # close_connection(conn)

        return redirect("/")
        
        
    
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



