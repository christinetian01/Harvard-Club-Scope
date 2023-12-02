from flask import Flask, render_template, redirect, request, session
from flask_session import Session
import requests
import psycopg2
from bs4 import BeautifulSoup
import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps

app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

conn = psycopg2.connect(database = "clubs", user = "postgres", password = "cs50harvardsc0pE2023", host = "localhost", port = "5432")
db = conn.cursor()

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

def club_scrape():

    URL = "https://csadvising.seas.harvard.edu/opportunities/clubs/"
    page = requests.get(URL)

    soup = BeautifulSoup(page.text)

    wrap_div = soup.find("div", {"class":"padding highlightable"})
    clubs = wrap_div.find("div", {"id":"body-inner"}).find_all('li')

    for club in clubs:
        db.execute("INSERT INTO club_names SELECT (%s) WHERE NOT EXISTS (SELECT * FROM club_names WHERE clubname = (%s))", (club.find('a').text, club.find('a').text))
        conn.commit()

club_scrape()
db.execute("SELECT * FROM club_names")
clubs = db.fetchall()

@app.route("/", methods=["GET", "POST"])
@app.route('/')
def index():
    years = []
    year = datetime.date.today().year
    for i in range(10):
        years.append(year+i)

    if request.method == "GET":
        return render_template("homepage.html", years = years, message = "Click to see events!")
    
    date = request.form.get('cell')
    db.execute("SELECT * FROM events WHERE date = %s", (date, ))
    events = db.fetchall()

    return render_template("homepage.html", years = years, events = events, message = "Events for " + date)
    

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("clubname"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        db.execute(
            "SELECT * FROM registered_clubs WHERE clubname = %s", (request.form.get("clubname"),)
        )
        rows = db.fetchall()

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0][3], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0][0]

        # Redirect user to upcoming events
        return redirect("/upcoming_events")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html", clubs = clubs)
    


@app.route("/register", methods = ["GET", "POST"])
def register():
    """Register user"""

    if request.method == "GET":
        return render_template("register.html", clubs = clubs)

    # getting the username and confirmation
    # not storing password for cybersecurity reasons
    clubname = request.form.get("clubname")
    confirm = request.form.get("confirmation")
    bio = request.form.get("bio")

    # username wasn't entered
    if not clubname:
        return render_template("register.html", success_error = "Please select a club!", clubs = clubs)
    # password wasn't entered
    if not request.form.get("password"):
        return render_template("register.html", success_error = "Please enter a password!", clubs = clubs)
    if not bio:
        return render_template("register.html", success_error = "Please enter a short club bio!", clubs = clubs)
    # password wasn't confirmed
    if not confirm:
        return render_template("register.html", success_error = "Please confirm your password!", clubs = clubs)
    # password confirmation doesn't match
    if request.form.get("password") != confirm:
        return render_template("register.html", success_error = "Confirmation password didn't match! Please re-enter!", clubs = clubs)

    # hash the password
    hash_pass = generate_password_hash(request.form.get("password"))

    # insert new username and password into users table
    try:
        db.execute("INSERT INTO registered_clubs (clubname, bio, password) VALUES (%s, %s, %s)", (clubname, bio, hash_pass))
        conn.commit()
    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        return render_template("register.html", success_error = "This club has already registered", clubs = clubs)

    #WHY DOES THE PAGE CRASH WHEN I RELOAD
    return redirect('/')

@app.route("/add_event", methods = ["GET", "POST"])
@login_required
def add_event():
    if request.method == "GET":
        return render_template("add_event.html")

    event_name = request.form.get("event_name")
    description = request.form.get("description")
    loc = request.form.get("loc")
    street = request.form.get("street")
    city = request.form.get("city")
    state = request.form.get("state")
    zip_code = request.form.get("zip")
    room_number = request.form.get("room_num")
    date = request.form.get("date")
    time = request.form.get("time")
    
    db.execute("SELECT clubname FROM registered_clubs WHERE id = %s", (session["user_id"], ))
    club_name = db.fetchall()[0]

    db.execute("INSERT INTO events VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (session["user_id"], club_name, event_name, description, loc, street, city, state, zip_code, room_number, date, time))
    conn.commit()

    return redirect("/upcoming_events")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

if __name__ == "__main__":
    app.run(debug = True)


@app.route("/upcoming_events", methods = ["GET"])
@login_required
def upcoming_events():
    db.execute("SELECT * FROM events WHERE id = %s ORDER BY date, time", (session["user_id"], ))
    events = db.fetchall()

    return render_template("upcoming_events.html", events = events)

