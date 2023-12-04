
<h1>app.py</h1>
At the very beginning of the file, I imported all of the necessary libraries and packages. I then initialized a Flask app session. After that, I connected to my clubs database housed on PostgreSQL using the connect function from psycopg2 and providing the relevant authorization information. Then, I opened a cursor using the cursor() function that allows me to execute SQL queries through Python.  

<h2>login_required()</h2>
This is a helper function that is meant to prevent users from accessing certain pages if a user is not logged into an account. It can be added as a decorator to routes that should only be accessible by logged in users. This function was directly copied from “Finance” on Problem Set 9. 
<h2>club_scrape()</h2>
This function is used for scraping the website https://csadvising.seas.harvard.edu/opportunities/clubs/ to get a list of the CS club names that will be used as select options when registering a club or logging into a club. I decided against using an input box for the club name on these pages because the same club can go by multiple names, which will make it hard to determine whether a club has already been registered. For example, HCS can also be inputted as Harvard Computer Society. If there’s a lapse in communication between people registering for an account, they’d be able to create two accounts for the same club. club_scrape() is meant to get these club options by using the Python package BeautifulSoup.
<ol>
<li> First, I sent an HTTP request to https://csadvising.seas.harvard.edu/opportunities/clubs/, which then returns the HTML of the page in a string format. 
<li> The HTML is then parsed using the BeautifulSoup() function, which essentially takes the HTML and creates a BeautifulSoup() object that allows me to search through the HTML for specific elements rather than having to search through the string that is returned in step 1. 
<li> In order to access the club names, I had to go through two levels of div elements, which I determined through inspecting the club website. The first parent div was of class “padding highlightable”, which allowed me to extract it by focusing on the class name. After that, I searched the parent div for another div with the id “body-inner”, and searched that div for all of the li elements, which contain the club names. 
<li> The code then extracts all of the li items and loops through them to extract the text of the anchor element, which isolates the actual club name.
<li> The text of the anchor elements was then inserted into the club_names database. I added a condition to the query that inserts the club only if it’s not already present in the database. This is so that everytime the page runs, there aren’t any duplicates, but it also allows for the addition of new clubs if the website is updated. 
club_scrape() is run independently of any other functions to allow for updating the database if new clubs are added. 
</ol>
<h2>index()</h2>
<ol>
<li>I wanted the calendar to be able to display over 10 years, starting from the current year. I used datetime.date.today().year to get the current year, and then used a for loop to obtain the next 10 years, each of which was appended into a years list. 
<li>If the request method is GET, then the page renders “homepage.html” with the years generated above as a Jinja input. The request method being GET also implies that the user hasn’t selected any dates yet, so the date argument is assigned an empty string (see why in calendar.js) and the message argument is assigned  “Click to see events”, which will be displayed below the calendar. 
<li>If the code reaches anywhere beyond the if statement for GET, that implies that a POST request was made. Essentially, the user has clicked a day on the calendar. Because each day/cell is implemented as a button (see why in calendar.js), retrieving the value of the cell will return the corresponding day.
<li>Select all of the events in the events table where the date is equal to the date extracted from above. 
<li>Render the homepage template with the date, events, and a message saying “Events for DATE” as Jinja inputs.  
</ol>
<h2>login()</h2>
For the login() function, I used the same function from Finance. The only things that have changed are as follows:
<ol>
<li>If there is an error with the log in, I render the “error.html” template with a relevant error message. 
<li>If the login is successful, the user is redirected to the “upcoming_events” page. 
<li>Because of the differences between psycopg2’s execute and cs50’s execute, I had to add some additional lines of the code such as rows = db.fetchall() that would get the results of the SQL queries. 
<li>I changed the first if statement to check if the request method is a GET instead of a POST. I think this makes the code more readable since the GET process is much shorter than the POST process, so the code is just more readable this way. 
<li>Rendering the login page takes in clubs as an argument because the club names are displayed as a select menu instead of an input box (see why in club_scrape())
</ol>
<h2>register()</h2>
This function handles the events on the registration page. 
<ol>
<li>If the request method is GET, then register.html is rendered with the clubs as an input so that they’re displayed in the select form. Similar to my reason for login(), the if statement determines if the request method was GET instead of POST to make the code more readable. 
<li>If any code beyond the first if statement is executed, then the request method is a post, meaning that a user has submitted the form on register. 
<li>The next step is input validation. In particular, we need to check if a club name was selected, if a password was entered, if a confirmation password was entered, and if a club bio was entered. If any of these aren’t true, then the user is met with an error message (error.html) that contains a relevant message
<li>If all of the inputs are validated, the entered password is hashed for increased security. 
<li>All of the information is then entered into the registered_clubs database
The ‘clubname’ column of the registered_clubs table is unique, so if the user tries to register a club that has already been registered, then an error will arise with the query. So, I added a try and except clause to look out for users that violate the unique property. If the query fails, then the attempted execution is rolled back (if it isn’t rolled back, then subsequent queries will fail), and the user is met with an error message. 
<li>Successfully registering a club will redirect the user to the homepage. 
</ol>
<h2>add_event()</h2>
<ol>
This function handles the events on the add events page. Through this, clubs can schedule events that will be displayed on the homepage calendar. This page is only visible to clubs that have logged in. 
<li>If the request method is GET, then add_event.html is rendered. Similar to my reason for login(), the if statement determines if the request method was GET instead of POST to make the code more readable. 
<li>If any code beyond the first if statement is executed, then the request method is a post, meaning that a user has submitted the form on add_event. 
<li>The next step is input validation. In particular, we need to check if an event name, event description, location, room number, date, and time was entered. If any of these aren’t true, then the user is met with an error message (error.html) that contains a relevant message. It also returns an error if the inputted date has already passed. 
<li>If all the inputs are validated, a query is run to get the name of the club that just submitted the event. We want to input the club name into the events table because when a user clicks on the date, we also want the club name to show up for each event. Although we could use a query that maps the club ids to the names, this wouldn’t be too practical when we’re actually trying to input the information into the table. The club name should be in the same row as the event information, and since the HTML generates each table row in its entirety, it would be impractical to create a row and only put in the club names, and then somehow go back to the beginning to input the event information. It’s worth noting that using an approach of this nature would still require the same amount of queries to be made. 
<li>The information for the event is then inputted into the events table and committed. It is worth noting that each event will have an event id that will come in handy when a club wants to edit one of their events. 
</ol>
<h2>logout()</h2>
The logout function simply clears the session and redirects the user to the homepage. 
<h2>upcoming_events()</h2>
upcoming_events() displays the upcoming events of a club. It is only visible to users who have logged in. Because there are no forms on this page, upcoming_events only handles GET requests. When a user navigates to the page, an SQL query that selects all of the club’s events (if the id matches the session’s user id) that are either happening on the current day or in the future. It is worth noting that the time is not taken into account when displaying the page. That is, if an event happened at 3:00 pm on a given day and it is currently 6:00 pm, the 3:00 pm would still be displayed because it took place on the same day. These events are then sent to “upcoming_events.html”, which is then rendered for the user to view. Each row of the upcoming events also contains an edit button that is connected to the page “edit_events_direct”. The value of the button is the event id. More on this in the edit_events_direct() and edit_events() section. 
<h2>edit_bio()</h2>
edit_bio() allows clubs to edit their club bios in case there are changes to how the club is run. Once again, I put the GET conditional at the very top and put the POST steps right after the GET return statement. In the GET method, I executed a query that retrieves the club’s current bio and sends it to be displayed in “edit_bio.html”. I implemented it this way instead of just having an empty input because more often than not, there’s only going to be small edits to the bio. It would be inefficient if the user would have to start from scratch every time they wanted to make just a tiny modification. 
<br></br>
For a POST request, the text the user entered is retrieved. The validation step ensures that the textbox was not left blank. Then, an SQL query that updates the club’s information in registered_clubs is executed and committed. The user is then redirected to the homepage. 
<h2>edit_events_direct() and edit_events()</h2>
Both of these functions only handle POST requests. <br></br>
If a club wanted to edit one of their events, they’d be able to by navigating to the upcoming_events page and clicking the edit button that corresponds to the event they want to modify. Clicking this button will return the event id (which is stored as the value of the button). No validation is necessary for this because each entry of the SQL table will always have an event id, so the button is guaranteed to have a value.  The event corresponding to the event id is then retrieved from the events table and then inputted into edit_events_direct.html through Jinja. The event id is stored as the value of an invisible div for reasons that will be discussed in edit_events(). This will render a form similar to the one in add_event(), except the input fields will have the original values in them for the exact same reason I outlined in edit_bio(). <br></br>
The information submitted through the form is then sent to “/edit_events”, and all of the form inputs are retrieved. This includes the value of the invisible div, which stores the event id.  All of the other inputs go through the same input validation as that of add_event(). If there are no errors, the entry in events that corresponds to the event id we stored in the invisible div is updated with all of the inputted information. The user is then redirected to “/upcoming_events”, which will display the updated event information. 
<h2>explore_clubs()</h2>
	/explore_clubs is a page available to users without an account that allows them to view the bios of all the registered clubs. Because there is no form on this page, the function only handles GET requests. An SQL query that retrieves the club name and bio of every single entry is executed, and these entries are inputted into “explore_clubs.html”. 
<h2>all_upcoming_events()</h2>
/all_upcoming_events is a page available to users without an account that allows them to view all upcoming events in a table format. Because there is no form on this page, the function only handles GET requests. An SQL query that retrieves the event information of every single entry occurring on the current day or days after is executed, and these entries are inputted into “all_upcoming_events.html”. 
<h1>static folder</h1>
<h2>calendar.js</h2>
calendar.js is responsible for generating the interactive calendar that appears on the homepage (/) of the website. 
<ol>
<li>I added an event listener to ensure that the functions in the file only run once all of the HTML is loaded. 
<li>The current year and month are both stored in two variables, selectedYear and selectedMonth, that will be used as the input parameters when the calendar function is run at the very end. 
<li>On “homepage.html”, there is an invisible div element that stores the date a user clicks on in the YYYY-MM-DD format. If the value of the div element is empty, that indicates that the user has just navigated to the homepage and hasn’t actually selected any dates for the calendar to display. selectedYear and selectedMonth will remain the current year and month. If the user has selected a date, I used Jinja to input these into the invisible div so that calendar.js can access it and set selectedYear and selectedMonth to the corresponding year and month. I did this because each time a date is clicked, the page is re-rendered. Without this part of the code, each time a date is clicked, the re-rendering will switch the calendar back to the one corresponding to the current month and year. With this, when the page is re-rendered, the calendar still displays the appropriate one for the desired month and year. 
The corresponding lines of code select the dropdown elements that allow the user to switch between month and year. 
<h3>calendarGrid(month, year)</h3>
<li>These lines of code access the month_text and year_text header elements and alter the innerHTML of them so that the selected month and year are both displayed. 
<li>I then selected the calendar body div and determined whether it already contained child nodes. If it did, then the code removes all of them. If the child nodes weren’t cleared, then every time the user changes the month and year, the calendar would just append the new cells to the end of the old calendar. 
<li>The code then gets which day of the week the selected month starts on in addition to the number of days the month contains. 
<li>Because I wanted the calendar to be formatted such that the overall calendar body remained the same, I had to add some filler div elements to the beginning of the calendar depending on what day of the week the month starts on. This appears as white space on the calendar. 
<li>Because the code had already obtained the number of days in a given month, I used a for loop to generate a cell for each of these days. Each cell consists of a form with a button, and this was done so that each time a user clicks on a date, the page will re-render with the day’s events displayed at the bottom of the page. The form posts information to the homepage (/) when the corresponding button is clicked, so I set the form’s method to “post” and the action to “/”. 
<li>A button is created alongside each form, and the value of the button is the date that has been selected, which can be obtained since the function takes the month and year as inputs, and the specific day corresponds to the iteration of the for loop. The button’s innerHTML is altered so that it displays the corresponding day. The button is then appended to its respective form. 
<li>Every row of the calendar should only have 7 cells (including the filler). To ensure this, I used the condition i%7 == (7-firstDay), where i is the for loop iteration, to determine when to add a line break that starts the next row of the calendar. 
<li>At the end of the loop, the form is appended to the calendar body. 
<h3>changeMonth(event)</h3>
<li>changeMonth() is a function that regenerates the calendar when the user changes the month. Each option of the select element has a value that is in the months array declared at the beginning of calendar.js. The index of the value corresponds to the month index. calendarGrid() is run every time the month is changed, and the selected month is inputted. 
<li>changeYear() is a function that regenerates the calendar when the user changes the month. Each option of the select element has a value equal to the corresponding year, which can be extracted and set to selectedYear. calendarGrid() is run every time the year is changed, and the selected year is inputted. 
These lines of code add event listeners to the select menus that trigger changeMonth() and changeYear() whenever the month or year is changed. 
</ol>
<h2>styles.css</h2>
Contains the styling for all HTML elements
<h1>templates folder</h1>
Contains all of the HTML templates that have been referenced throughout
