from flask import Flask, render_template, redirect, request, session
from flask_session import Session
import requests
import psycopg2
from bs4 import BeautifulSoup
import sqlite3

app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

connection = sqlite3.connect("clubs.db", check_same_thread = False)
db = connection.cursor()

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
        clubs = db.execute("SELECT * FROM club_names")
        connection.close()
        return render_template("register.html", clubs = clubs)

def club_scrape():

    URL = "https://csadvising.seas.harvard.edu/opportunities/clubs/"
    page = requests.get(URL)

    soup = BeautifulSoup(page.text)

    wrap_div = soup.find("div", {"class":"padding highlightable"})
    clubs = wrap_div.find("div", {"id":"body-inner"}).find_all('li')

    for club in clubs:
        db.execute("INSERT INTO club_names VALUES (?)", (club.find('a').text,))
        connection.commit()
    
club_scrape()

if __name__ == "__main__":
    app.run(debug = True)