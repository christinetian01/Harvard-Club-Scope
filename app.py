from flask import Flask, render_template, redirect, request, session
from flask_session import Session

app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/')
def index():
    years = []

    for i in range(10):
        years.append(2023+i)

    return render_template("homepage.html", years = years)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    if request.method == "POST":

        # Forget any user_id
        session.clear()
        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/register", methods = ["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")

    # getting the username and confirmation
    # not storing password for cybersecurity reasons
    username = request.form.get("username")
    confirm = request.form.get("confirmation")

    # username wasn't entered
    if not username:
        return apology("Please enter a username!")
    # password wasn't entered
    if not request.form.get("password"):
        return apology("Please enter a password!")
    # password wasn't confirmed
    if not confirm:
        return apology("Please confirm your password!")
    # password confirmation doesn't match
    if request.form.get("password") != confirm:
        return apology("Confirmation password didn't match! Please re-enter!")

    # hash the password
    hash_pass = generate_password_hash(request.form.get("password"))

    # insert new username and password into users table
    try:
        db.execute(
            "INSERT INTO users (username, hash) VALUES (?, ?)", username, hash_pass
        )
    except ValueError:
        return apology("This username is taken! Please enter another!")

    return redirect("/")


if __name__ == "__main__":
    app.run(debug = True)