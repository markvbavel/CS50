import os
import sqlite3
import secrets  

from flask import Flask, flash, jsonify, redirect, render_template, request, session, g, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from markupsafe import escape

from helpers import apology, login_required, connect_db, close_connection, dict_factory, del_user, del_entry
from helpers import insert_student, insert_user, search_user, search_student, mod_user, get_headers, student_overview


# Configure application
app = Flask(__name__)

# Configure SqLite3 database
database = ("database.db")

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
@app.route("/", methods =["GET"])
@app.route("/index", methods =["GET"])
@login_required
def index():

    """Show overview of all students in a table"""
    print("INDEX GET")
            
    # Connect to database 
    conn = connect_db(database)
    conn.row_factory = dict_factory

    # Establish number of casts
    student_cast = 2

    # Select all student data
    headers = get_headers(conn)
    records = student_overview(conn)
    
    # If no data is present
    if not records:              
        return render_template("index.html", 
                                session = session, 
                                student_cast = student_cast,
                                headers = headers)

    # Change "None" to "-" for readability
    for record in records:
        for value in record:
            if record[value] == None:
                record[value] = "-"

    #Close db connection
    close_connection(conn)
    return render_template("index.html", 
                        session = session, 
                        records = records, 
                        headers = headers,
                        student_cast = student_cast)



# Login route
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # User reached route via POST
    if request.method == "POST":

        print("LOGIN POST")
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
        
        # Remember which user has logged in
        session["user_id"] = records[0]["id"]
        session["username"] = records[0]["username"]

        # Close database connection
        close_connection(conn)

        # Redirect user to home page
        return redirect(url_for("index"))

    # User reached route via GET
    else:
        print("LOGIN GET")
        # Student classes   
        student_classes = ["Junior", "Oranje", "Paars", "Blauw", "PG", "Demo", "Vakklas"]

        session["student_classes"] = student_classes

        return render_template("login.html")



# Logout route
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to home
    return redirect(url_for(("index")))



# Register route
@app.route("/register", methods=["GET", "POST"])
def register():
    
    # Clear any user id
    session.clear()

    if request.method == "POST":

        print("REGISTER POST")

        # Connect to database 
        conn = connect_db(database)
        conn.row_factory = dict_factory

        # Get username and password from form
        username = request.form.get("register_username")
        password = request.form.get("register_password")

        # Error check
        if not username or not password or not request.form.get("register_confirm"):
            return apology("Please fill in all fields", 401)
        
        if password != request.form.get("register_confirm"):
            return apology("Passwords don't match", 401)

        records = search_user(conn, username)
        if len(records) != 0:
            return apology("Username already exists", 409)
        
        # Error check passed. Insert user into users database
        user_data = (username, generate_password_hash(password))
        user_id = insert_user(conn, user_data)

        # Remember user
        session["user_id"] = user_id
        session["username"] = username

        # Close database connection
        close_connection(conn)
                
        # Redirect user to home
        return redirect(url_for("index"))
            
    else:
        print("REGISTER GET")
        return render_template("index.html")



@app.route("/new", methods = ["GET", "POST"])
@login_required
def new():
    """ Adds new students to students table """

    if request.method == "POST":
        print("NEW POST")
        
        # Connect to database 
        conn = connect_db(database)
        conn.row_factory = dict_factory

        # Gather data from form and put into a tuple
        student_data = (\
            request.form.get("new_firstname"),\
            request.form.get("new_lastname"),\
            request.form.get("new_birth"),\
            request.form.get("new_class"),\
            request.form.get("new_phone_1"),\
            request.form.get("new_phone_2"),\
            request.form.get("new_email_1"),\
            request.form.get("new_email_2"),\
            request.form.get("new_cast"),\
            request.form.get("new_role"),\
            request.form.get("new_notes"))

        # Insert into database
        insert_student(conn, student_data)

        flash("Student added!")

        return redirect(url_for("index"))

    else:
        print("NEW GET")
        return render_template("index.html")    



@app.route("/search", methods = ["POST"])
@login_required
def search():
    """ Searches student """

    # Connect to database 
    conn = connect_db(database)
    conn.row_factory = dict_factory

    if request.method == "POST":

        print("SEARCH POST")
        # Get search query
        query = str(request.form.get("search_searchbar"))
        column = request.form.get("search_class")
        
        # Query databse
        records = search_student(conn, query, column)

        # Get headers from databse
        headers = get_headers(conn)

        # Number of casts
        student_cast = 2

        # Close database connection
        close_connection(conn)

        return render_template("index.html",
                                session = session,
                                headers = headers, 
                                records = records,
                                student_cast = student_cast)



@app.route("/user", methods = ["GET", "POST"])
@login_required
def user():
    """
    Displays user information. User can edit username and password
    """

    # Connect to database 
    conn = connect_db(database)
    conn.row_factory = dict_factory

    if request.method == "POST":
        # To update user data
        print("USER POST")

        # Gather data
        user_id = session["user_id"]
        username_old = session["username"]
        username_new = request.form.get("user_username")
        pw_old = request.form.get("user_old_pw")
        pw_new = request.form.get("user_new_pw")
        pw_confirm = request.form.get("user_new_confirm")
        user_data = (username_new, generate_password_hash(pw_new))

        # Compare input to existing data
        records = search_user(conn, username_old)
        if check_password_hash(records[0]["hash"], pw_old) == False:
            return apology("Invalid password", 401)
        
        if pw_new != pw_confirm:
            return apology("Passwords don't match", 401)
        
        # Update user data
        mod_user(conn, user_data, user_id)
        close_connection(conn)

        flash("Profile updated!")
        
        return redirect(url_for("index"))

    else:
        # Display user data
        print("USER GET")
        return render_template("user.html")



@app.route("/delete/<int:entry_id>", methods = ["GET"])
@login_required
def delete_entry(entry_id):
    """
    Deletes entry data
    """
    print("DELETE ENTRY GET")

    conn = connect_db(database)
    conn.row_factory = dict_factory

    # Function call
    del_entry(conn, entry_id)
    close_connection(conn)

    flash("Entry deleted!")

    return redirect(url_for("index"))


@app.route("/user/delete/<int:user_id>", methods = ["GET"])
@login_required
def user_delete(user_id):
    """
    Deletes user account
    """

    print("DELETE USER GET")

    # Connect to database 
    conn = connect_db(database)
    conn.row_factory = dict_factory

    # Function call
    del_user(conn, user_id)
    close_connection(conn)

    flash("Profile deleted!")

    return redirect(url_for("logout"))



def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)

# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)