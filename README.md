# Harvard CScope README

Video: https://youtu.be/Mry0uttMfJA 

Harvard CScope is a web app through which students at Harvard can explore CS clubs (currently limited to the clubs listed on https://csadvising.seas.harvard.edu/opportunities/clubs/ ) and Harvard CS club leaders can publicize their club events. This was intended to make club event dates easier to track and negate the need for a large amount of emails publicizing the event. Currently, many CS club events are publicized through the HCS emailing list. If someone is interested in attending and wants to keep track of it, they would probably have to do something along the lines of manually entering the event into their Google Calendar. This process can get irritating if someone wants to attend multiple events. 

Harvard CScope allows clubs to create accounts through which they can submit information about their upcoming events, which will be visible to everyone using the app through an interactive calendar or a simple table. It is also flexible in that it allows clubs to edit their events in case things like the date or location changes. 

---------------------------------------------------------------------------------------------------------------------

Harvard CScope uses Python Flask, SQL, HTML, Javascript, and CSS. To run on VSCode, it requires the installation of Flask, a library called BeautifulSoup that will be for web scraping, and a library called psycopg2 that will be used to perform operations on PostgreSQL through Python (provided functionality similar to that of db.execute() shortcut in cs50.dev). 

## Flask Installation
I installed Flask following the [tutorial](https://code.visualstudio.com/docs/python/tutorial-flask), but I ran into a few additional issues that I will show how to resolve.

In VSCode, install the Python extension, and ensure that you have a version of Python 3 installed. In order to install Python 3, visit [python.org](https://www.python.org/downloads/), and install the version corresponding to your OS. 

When installing, there should be an option that says to “add python.exe to PATH”. Select this option and begin the installation. 

In order to check if Python was successfully installed, go to your terminal and type

<p style="text-align: center;">python –version</p>

It was at this point that I got the following error message:
Python was not found; run without arguments to install from the Microsoft Store, or disable this shortcut from Settings > Manage App Execution Aliases. 

<p style="text-align: center;">In Windows, this error arises when the location of the Python interpreter is not included in the PATH environment variable, which can happen if the above option was selected. To resolve this problem, I followed this <a href = https://www.youtube.com/watch?v=BatXXsIn6Xw&ab_channel=MohammedSadik>video</a>, which is specifically meant for Windows. </p>

1. Search for the Run command and enter “appdata” when  prompted for the name of the program. 
2. Open the “Local” folder, then the “Programs” folder, and then the “Python” folder. 
3. Copy the path of the “Python” folder. 
4. On the explore panel of the folder, right click “This PC” and click on “Properties”
5. In properties, click on “Advanced system settings” and click on “Environment Variables”. 
6. In the bottom of the popup window, there should be a section titled “System variables”. Find “Path” in “System variables” and click “Edit” once selected. 
7. In the new popup window, click “New”, paste the copied file path, and click “Ok”. 
8. Once this is done, go back to the “Python” folder found in step 2. Copy the path of the “Scripts” folder. 
9. Add the “Scripts” path PATH by following steps 6-7 again. 
10. After following these steps, running python –version should run successfully and return “Python 3.12.0” (depends on which version). 

## Beautiful Soup Installation
Beautiful Soup is a Python HTML parser package that I used to scrape the Harvard CS website for the club names. 

First navigate to the correct folder with the code files. If pulling from the GitHub repository, navigate to the folder using the command
<p style="text-align: center;">cd Harvard-Club-Scope</p>
Then, install Beautiful Soup with the command
<p style="text-align: center;">pip install beautifulsoup4</p>
This will successfully install the Beautiful Soup library. 

## psycopg2 Installation
psycopg2 is a Python library that I used to run queries and interact with my databases housed on PostgresSQL. Through it, I was able to run commands similar to that of “db.execute()” with just a few slight modifications. 

To install psycopg2, run the following command in the terminal:
<p style="text-align: center;">pip install psycopg2-binary</p>
This will successfully install psycopg2 and will allow you to connect to a database housed on PostgresSQL and execute queries through Python. 

---------------------------------------------------------------------------------------------------------------------
Running the Project
After installing all the libraries and packages delineated above, first ensure that you have navigated to the folder containing the file “app.py”. This can be done using the command
<p style="text-align: center;">cd folder name</p>
Having navigated to the correct folder, run the project by executing the command
<p style="text-align: center;"> run flask </p>

The following should appear once “flask run” has been executed. Open up the web app by clicking on the link provided above. 

