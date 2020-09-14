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

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

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
Session(app)



# Home route
@app.route("/")
def index():
    """Show overview of all students in a table"""
    if request.method == "POST":

        """TODO"""
        """ 
        - Get search query
        - Run query on students database
        - return results
        - dispaly results on index.html
        """

        return redirect("/")    

    else:
        return render_template("index.html", session = session)



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
        password = request.form.get("login_password")

        # Error checking on user input
        if not username or not password:
            return apology("Please fill in all the required fields", 403)

        # Query users table for username
        records = search_user(conn, username)

        # Ensure username exists and password is correct
        if len(records) != 1:
            return apology("username not found", 401)
        elif check_password_hash(records[0]["hash"], password) == False:
            return apology("Invalid password", 401)

        print("records[0]hash: ", records[0]["hash"])
        
        # Remember which user has logged in
        session["user_id"] = records[0]["id"]
        session["username"] = records[0]["username"]

        print("session user_id: ", session["user_id"])

        # Close database connection
        close_connection(conn)

        flash("Logged in")

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

    # Redirect user to home
    return redirect("/")



# Register route
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        # Clear any user id
        session.clear()

        # Connect to database 
        conn = connect_db(database)
        conn.row_factory = dict_factory

        # Get username and password from form
        username = request.form.get("register_username")
        password = request.form.get("register_password")

        # Error check
        if not username or not password or not request.form.get("register_confirm"):
            flash("Please fill in all fields")
            return redirect("/register")
        
        if password != request.form.get("register_confirm"):
            return apology("Passwords don't match", 401)

        records = search_user(conn, username)
        if len(records) != 0:
            return apology("Username already exists", 409)
        
        # Error check passed. Insert user into users database
        """ TODO """
        user_data = (username, generate_password_hash(password))
        user_id = insert_user(conn, user_data)
        print("user_id", user_id)

        # Close database connection
        close_connection(conn)
        
        flash("Signed up!")
        
        # Redirect user to home
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



