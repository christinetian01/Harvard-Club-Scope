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

# connect to clubs database on PostgreSQL
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

    # scrape the CS website
    URL = "https://csadvising.seas.harvard.edu/opportunities/clubs/"
    # 1. HTTP request that returns the HTML of the page
    page = requests.get(URL)

    # 2. parses the HTML, creating a tree structure of the HTML data
    soup = BeautifulSoup(page.text)

    # 3. can't access the club divs directly, so need to access the parent div first
    wrap_div = soup.find("div", {"class":"padding highlightable"})
    # access the divs that contain the club information
    clubs = wrap_div.find("div", {"id":"body-inner"}).find_all('li')

    # 4. for each of the different divs, extract the club name stored in an <a> element
    for club in clubs:
        # 5. insert the extracted name into the club_names table if it doesn't already exist
        db.execute("INSERT INTO club_names SELECT (%s) WHERE NOT EXISTS (SELECT * FROM club_names WHERE clubname = (%s))", (club.find('a').text, club.find('a').text))
        # commit the insertion
        conn.commit()

# running everytime the page is opened in case the website is updated with new clubs
club_scrape()

# getting all of the club names
db.execute("SELECT * FROM club_names")
clubs = db.fetchall()


@app.route("/", methods=["GET", "POST"])
def index():
    
    # 1. should generate years starting from current until current + 10years
    years = []
    year = datetime.datetime.today().year
    for i in range(10):
        years.append(year+i)

    # 2. render homepage with the default values
    if request.method == "GET":
        return render_template("homepage.html", date = '', years = years, message = "Click to see events!")
    
    # 3. render homepage for the selected date
    date = request.form.get('cell')
    # 4. get all the events that are on the selected date
    db.execute("SELECT * FROM events WHERE date = %s ORDER BY time", (date, ))
    events = db.fetchall()

    # 5. render homepage with the relevant information
    return render_template("homepage.html", date = date, years = years, events = events, message = "Events for " + date)
    

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via GET (as by clicking a link or via redirect)
    if request.method == "GET":
        return render_template("login.html", clubs = clubs)

    # User reached route via POST (as by submitting a form via POST)
    # Ensure username was submitted
    if not request.form.get("clubname"):
        return render_template("error.html", message = "must provide club name")

    # Ensure password was submitted
    elif not request.form.get("password"):
        return render_template("error.html", message = "must provide password")

    # Query database for username
    db.execute(
        "SELECT * FROM registered_clubs WHERE clubname = %s", (request.form.get("clubname"),)
    )
    rows = db.fetchall()

    # Ensure username exists and password is correct
    if len(rows) != 1 or not check_password_hash(
        rows[0][3], request.form.get("password")
    ):
        return render_template("error.html", message = "invalid username and/or password")

    # Remember which user has logged in
    session["user_id"] = rows[0][0]

    # Redirect user to upcoming events
    return redirect("/upcoming_events")
    


@app.route("/register", methods = ["GET", "POST"])
def register():
    """Register user"""

    # 1. if the request method is GET, render register.html
    if request.method == "GET":
        return render_template("register.html", clubs = clubs)

    # 2. request method is POST

    # getting the username and confirmation
    # not storing password for cybersecurity reasons
    clubname = request.form.get("clubname")
    confirm = request.form.get("confirmation")
    bio = request.form.get("bio")

    # 3. input validation
    # clubname wasn't entered
    if not clubname:
        return render_template("error.html", message = "Please select a club!")
    # password wasn't entered
    if not request.form.get("password"):
        return render_template("error.html", message = "Please enter a password!")
    if not bio:
        return render_template("error.html", message = "Please enter a short club bio!")
    # password wasn't confirmed
    if not confirm:
        return render_template("error.html", message = "Please confirm your password!")
    # password confirmation doesn't match
    if request.form.get("password") != confirm:
        return render_template("error.html", message = "Confirmation password didn't match! Please re-enter!")

    # 4. hash the password
    hash_pass = generate_password_hash(request.form.get("password"))

    # 5. insert new username and password into users table
    try:
        db.execute("INSERT INTO registered_clubs (clubname, bio, password) VALUES (%s, %s, %s)", (clubname, bio, hash_pass))
        conn.commit()
    # 6. error if the club has already registered
    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        return render_template("error.html", message = "This club has already registered")

    # 7. redirect to homepage
    return redirect('/')



@app.route("/add_event", methods = ["GET", "POST"])
@login_required
def add_event():

    # 1. if the user is routed to the page, then redner the add_event template
    if request.method == "GET":
        return render_template("add_event.html")

    # 2. POST
    event_name = request.form.get("event_name")
    description = request.form.get("description")
    loc = request.form.get("loc")
    room_number = request.form.get("room_num")
    date = request.form.get("date")
    time = request.form.get("time")

    # 3. input validation
    if not event_name:
        return render_template("error.html", message = "Please provide an event name")
    if not description:
        return render_template("error.html", message = "Please provide an event description")
    if not loc:
        return render_template("error.html", message = "Please provide an event location")
    if not room_number:
        return render_template("error.html", message = "Please provide a room number")
    if not date:
        return render_template("error.html", message = "Please provide a date")
    if not time:
        return render_template("error.html", message = "Please provide a time")
    
    # check if the date has already passed
    full_date_time = date +" "+time +":00"
    date_time = datetime.datetime.strptime(full_date_time.replace('-', '/'), '%Y/%m/%d %H:%M:%S')

    if date_time < datetime.datetime.today():
        return render_template("error.html", message = "That date/time has already passed!")
    
    # 4. get the clubname of the one that submitted the form
    db.execute("SELECT clubname FROM registered_clubs WHERE id = %s", (session["user_id"], ))
    club_name = db.fetchall()[0]

    # 5. insert the event information into the events table
    # each event will have an event id
    db.execute("INSERT INTO events VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (session["user_id"], club_name, event_name, description, loc, room_number, date, time))
    conn.commit()

    return redirect("/upcoming_events")



@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to homepage
    return redirect("/")


@app.route("/upcoming_events", methods = ["GET"])
@login_required
def upcoming_events():
    # selects events that are on the same day or on following days
    # only shows the club events
    db.execute("SELECT * FROM events WHERE club_id = %s AND date >= (SELECT date_trunc('day', NOW())) ORDER BY date, time", (session["user_id"], ))
    events = db.fetchall()

    return render_template("upcoming_events.html", events = events)


@app.route("/edit_bio", methods = ["GET", "POST"])
@login_required
def edit_bio():
        if request.method == "GET":
            # retrieve the current bio
            db.execute("SELECT bio FROM registered_clubs WHERE id = %s", (session["user_id"], ))
            bio = db.fetchall()[0]

            # displays the current bio
            return render_template("edit_bio.html", bio = bio)
        
        # get new bio
        new_bio = request.form.get("new_bio")
        # make sure new bio is not empty
        if not new_bio:
            return render_template("error.html", message = "Bio cannot be empty")

        # update registered_clubs with the new bio
        db.execute("UPDATE registered_clubs SET bio = %s WHERE id = %s", (new_bio, session["user_id"]))
        conn.commit()

        return redirect("/")


@app.route("/edit_events_direct", methods = ["POST"])
@login_required
def edit_events_direct():
    # get the id of the event they want to change
    event_id = request.form.get("edit_button")
    
    # retrieve the event with the event_id
    db.execute("SELECT * FROM events WHERE event_id = %s", (event_id,))
    event = db.fetchall()[0]

    return render_template("edit_events_direct.html", event = event)



@app.route("/edit_events", methods = ["POST"])
@login_required
def edit_events():
    # get the event id
    event_id = request.form.get("event_id")

    # get the form inputs
    event_name = request.form.get("event_name")
    description = request.form.get("description")
    loc = request.form.get("loc")
    room_number = request.form.get("room_num")
    date = request.form.get("date")
    time = request.form.get("time")

    # input validation
    if not event_name:
        return render_template("error.html", message = "Please provide an event name")
    if not description:
        return render_template("error.html", message = "Please provide an event description")
    if not loc:
        return render_template("error.html", message = "Please provide an event location")
    if not room_number:
        return render_template("error.html", message = "Please provide a room number")
    if not date:
        return render_template("error.html", message = "Please provide a date")
    if not time:
        return render_template("error.html", message = "Please provide a time")
    
    # check if the date has already passed
    full_date_time = date +" "+time +":00"
    date_time = datetime.datetime.strptime(full_date_time.replace('-', '/'), '%Y/%m/%d %H:%M:%S')
    
    if date_time < datetime.datetime.today():
        return render_template("error.html", message = "That date/time has already passed!")

    # update the event corresponding to the event id
    db.execute("UPDATE events SET name = %s, description = %s, locationname = %s, room_num = %s, date = %s, time = %s WHERE event_id = %s", (event_name, description, loc, room_number, date, time, event_id))
    conn.commit()

    return redirect("/upcoming_events")



@app.route("/explore_clubs", methods = ["GET"])
def explore_clubs():
    # selects all registered clubs
    db.execute("SELECT clubname, bio FROM registered_clubs")
    clubs = db.fetchall()

    # displays all the registered clubs
    return render_template("explore_clubs.html", clubs = clubs)



@app.route("/all_upcoming_events", methods = ["GET"])
def all_upcoming_events():

    db.execute("SELECT * FROM events WHERE date >= (SELECT date_trunc('day', NOW())) ORDER BY date, time")
    all_events = db.fetchall()

    return render_template("all_upcoming_events.html", all_events = all_events)