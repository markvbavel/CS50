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
app.jinja_env.filters["usd"] = usd # app.jinja_env.filters["usd"] = usd
app.jinja_env.globals.update(usd=usd)

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


@app.route("/", methods=["GET", "POST"])
@login_required
def index():

    user_id = session["user_id"]

    # Gets current ammount of cash
    user_cash = db.execute("SELECT cash FROM users WHERE id = :user_id",
                            user_id = user_id)[0]["cash"]

    # Copy user_cash to total_value to add stocks' current value later
    total_value = user_cash

    # Gets information on currently owned stocks
    user_stocks = db.execute("SELECT symbol, name, SUM(shares), current_price FROM stocks WHERE user_id = :user_id GROUP BY symbol HAVING SUM(shares) > 0 ORDER BY SUM(shares) DESC",
                              user_id = user_id)

    # Updates current_price to the latest price value
    for stock in user_stocks:
        stock["current_price"] = lookup(stock['symbol'])['price']
        total_value += stock["current_price"] * stock["SUM(shares)"]

    return render_template("index.html", user_stocks = user_stocks, user_cash = user_cash, total_value = total_value)

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """""Buy shares of stock"""

    # User reached route via POST
    if request.method == "POST":

        # Get values to work with
        quote = lookup(request.form.get("symbol"))
        shares = request.form.get("shares")
        ammount = quote["price"] * int(shares)
        user_id = session["user_id"]
        user_balance = float(db.execute("SELECT cash FROM users WHERE id = :user_id",
                                         user_id = user_id)[0]["cash"])

        # Idea for datetime insertion belongs to Tim Biegeleisen at Stack Overflow
        # https://stackoverflow.com/questions/29900785/inserting-datetime-into-a-sqlite-database
        time = str(datetime.now().strftime("%B %d, %Y %I:%M%p"))


        # print("quote {}".format(quote)) # prints {'name': 'Apple, Inc.', 'price': 455.59, 'symbol': 'AAPL'}
        # print("shares {}".format(shares)) # prints 1
        # print("ammount {}".format(ammount)) # prints 455.59
        # print("user_id {}".format(user_id)) # prints 6
        # print("user_balance {}".format(user_balance)) # prints 3505.16
        # print("time {}".format(time)) # prints date and time


        # Error checking
        if not quote:
            return apology("Invalid symbol", 403)

        elif int(shares) < 1:
            return apology("Provide a positive number", 403)

        elif ammount > user_balance:
            flash("Insufficient funds.")
            return redirect("/buy")

        # User can afford the transaction
        print("\n///// TRANSACTION APPROVED /////\n")

        insert = db.execute("INSERT INTO stocks (user_id, symbol, name, shares, price, time) VALUES (:user_id, :symbol, :name, :shares, :price, :time)",
                             user_id = user_id,
                             symbol = quote["symbol"],
                             name = quote["name"],
                             shares = shares,
                             price = quote["price"],
                             time = time)

        update = db.execute("UPDATE users SET cash = :new_balance WHERE id = :user_id",
                             new_balance = user_balance - ammount,
                             user_id = user_id)

        flash("Bought!")
        return redirect("/")

    # User reached route via GET
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # sold or bought
    # symbol
    # purchase or sale price
    # number of shares bought or sold
    # date and time of transaction

    # User only reaches this route via GET

    user_id = session["user_id"]

    user_stocks = db.execute("SELECT symbol, name, shares, price, time FROM stocks WHERE user_id = :user_id ORDER BY time DESC",
                              user_id = user_id)

    return render_template("history.html", user_stocks = user_stocks)


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

        flash("Login succesful")

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

        quote = lookup(symbol) # prints {'name': 'Netflix, Inc.', 'price': 475.47, 'symbol': 'NFLX'}

        # Return values of quote to quoted.html
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

        # Error checking
        if not request.form.get("username"):
            return apology("must provide username", 403)

        elif not request.form.get("password"):
            return apology("must provide password", 403)

        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords do not match", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                           username = request.form.get("username"))

        # Check if username exists
        if len(rows) > 0:
            return apology("Username is not available", 403)

        # Insert new user into database
        user_id = db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)",
                              username = request.form.get("username"),
                              hash = generate_password_hash(request.form.get("password")))

        # Remember current user
        session["user_id"] = user_id

        flash("Registration successful")

        # Redirect user to home
        return redirect("/")

    # User reached route via GET
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    # User reached route via POST
    if request.method == "POST":


        # Remember user
        user_id = session["user_id"]

        # Gets data on stock to be sold
        quote = lookup(request.form.get("symbol"))

        # Gets number of shares to be sold
        shares = int(request.form.get("shares"))

        # Rember users' cash value
        user_balance = db.execute("SELECT cash FROM users WHERE id = :user_id",
                                user_id = user_id)[0]["cash"]

        # Gets users' info on selected stock
        user_stock = db.execute("SELECT symbol, SUM(shares) FROM stocks WHERE (user_id = :user_id) AND (symbol = :symbol) GROUP BY symbol",
                                  user_id = user_id,
                                  symbol = quote["symbol"])[0]

        # Gets current time
        time = str(datetime.now().strftime("%B %d, %Y %I:%M%p"))


        # Check for errors
        if not quote:
            return apology("Enter a valid symbol", 403)

        elif not shares or shares < 1:
            return apology("Enter number of shares to sell", 403)

        elif quote["symbol"] != user_stock["symbol"]:
            return apology("You don't own any of this stock", 403)

        elif shares > user_stock["SUM(shares)"]:
            return apology("Can't sell that many shares", 403)

        # No errors occured
        print("\nTRANSACTION APPROVED\n")


        # Insert new row into stocks
        insert = db.execute("INSERT INTO stocks (user_id, symbol, name, shares, price, time) VALUES (:user_id, :symbol, :name, :shares, :price, :time)",
                             user_id = user_id,
                             symbol = quote["symbol"],
                             name = quote["name"],
                             shares = -shares,
                             price = -quote["price"],
                             time = time)

        # Update users' cash balance
        update = db.execute("UPDATE users SET cash = :new_balance WHERE id = :user_id",
                             new_balance = user_balance + (quote["price"] * shares),
                             user_id = user_id)

        flash("Sold!")
        return redirect("/")

    # User reached route via GET
    else:
        # Render users' currently owned symbols
        user_id = session["user_id"]
        user_symbols = db.execute("SELECT symbol FROM stocks WHERE (user_id = :user_id) GROUP BY symbol HAVING SUM(shares) > 0",
                                  user_id = user_id)

        return render_template("sell.html", user_symbols = user_symbols)

@app.route("/change")
@login_required
def change():
    """ Display change in users' owned stocks compared to yesterday """

    # User only reaches this route via GET

    # Gather user data
    user_id = session["user_id"]
    user_stocks = db.execute("SELECT symbol, name, current_price FROM stocks WHERE user_id = :user_id GROUP BY symbol HAVING SUM(shares) > 0 ORDER BY current_price DESC",
                              user_id = user_id)

    # Gets current price and adds change and changePercent to the dict
    for stock in user_stocks:
        stock['current_price'] = lookup(stock['symbol'])['price']
        stock['change'] = lookup(stock['symbol'])['change']
        stock['changePercent'] = "{:.2f}".format(lookup(stock['symbol'])['changePercent'])

    return render_template("change.html", user_stocks = user_stocks)#, changes = changes)

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
