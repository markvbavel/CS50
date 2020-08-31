import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """ loop over users' stock """

    """
    user_id = session["user_id"]
    rows = db.execute("SELECT symbol, name, shares FROM shares")

    for data in rows:
        print(data)
    """




    """Show portfolio of stocks"""
    return render_template("index.html", )


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """""Buy shares of stock"""

    # User reached route via POST
    if request.method == "POST":

        symbol = lookup(request.form.get("symbol"))
        shares = request.form.get("shares")
        rows = db.execute("SELECT cash FROM users WHERE id = :user_id",
                          user_id = session["user_id"])


        # If an ivalid symbol is entered
        if not symbol:
            return apology("Invalid symbol", 403)

        # If no positive integer provided in number of shares
        if int(shares) <= 0:
            return apology("Can't buy negative shares", 403)


        """
        TODO:
            - Acces:
                - request.form.get("Symbol")
                - request.form.get("Shares")
                - user_id = session["user_id"]
            - Check current users['cash']
            - Quote API key for symbol and price
            -

        """
        # Check if the share is not too expensive
        if rows[0]['cash'] < (symbol['price'] * int(shares)):
            return apology("Insufficient funds", 403)

        # Idea for datetime insertion belongs to Tim Biegeleisen at Stack Overflow
        # https://stackoverflow.com/questions/29900785/inserting-datetime-into-a-sqlite-database
        date = str(datetime.now().strftime("%B %d, %Y %I:%M%p"))
        print(date)

        # Insert data from the transaction into shares table
        db.execute("INSERT INTO shares (symbol, name, shares, price, time, user_id) VALUES (?, ?, ?, ?, ?, ?)",
                    request.form.get("symbol"),
                    symbol["name"],
                    request.form.get("shares"),
                    symbol["price"],
                    date,
                    session["user_id"])

        shares = db.execute("SELECT id FROM shares ORDER BY id DESC LIMIT 1")
        db.execute("INSERT INTO transactions (user_id, shares_id) VALUES (?, ?)",
                    session["user_id"],
                    shares[0]['id'])

        # Check if databases work
        test = db.execute("SELECT name FROM shares WHERE id IN (SELECT shares_id FROM transactions WHERE user_id IN (SELECT id FROM users WHERE username = :user_id))", user_id = session["user_id"])
        print(test)

        flash("Succes!")
        return redirect("/")

    # User reached route via GET
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    return render_template("history.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        flash("Logged in")
        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "POST":
        symbol = request.form.get("symbol")

        # Query API for symbol
        quote = lookup(symbol)
        # prints {'name': 'Netflix, Inc.', 'price': 475.47, 'symbol': 'NFLX'}

        return render_template("quoted.html", quote=quote)

    else:
        return render_template("quote.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via POST
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Ensure confirmation password matches
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords do not match", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username = request.form.get("username"))

        # Check if username exists
        if len(rows) == 1:
            return apology("Username is not available", 403)

        user_id = db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)",
                            username = request.form.get("username"),
                            hash = generate_password_hash(request.form.get("password")))

        # Remember current user
        session["user_id"] = user_id

        flash("Registered")
        # Redirect user to home
        return redirect("/")

    # User reached route via GET
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    return render_template("sell.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
