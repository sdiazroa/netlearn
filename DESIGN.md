# NetLearn

Languages used:
Python
SQL
Jinja
HTML
JavaScript
CSS

Overview & Framework

Our website uses the Flask framework and leverages bootstrap for designs similar to that of Finance. That framework uses application.py as the controller, contains a “templates” folder with the HTML files, and a static folder with CSS and any image files we used in our templates. Our crm.db SQL database has two tables, one called “users”, which stores users registered through the Create Account page, and one called “network”, which stores specific information users provide through the Add Info page after logging in to the site. The “werkzeug” library imported into application.py allows us to provide password protection in the form of hashes. Using the Flask framework allowed us to easily route to HTML templates that were each customized for the main sections of the site (Login, Create Account, SOM Network, Add Info, Quiz), and also allowed us to extend layout.html to all templates as to not make modifications for design in every html file. This can be seen at the top of each html template with the Jinja code {% extends “layout.html” %}.

Add Info & SOM Network

To input user data into the SOM network, we used Python to query (request.form.get) and save user input. We then stored user input into our Network table in SQL. To see Python and SQL code in detail, reference lines 121-136 of application.py. The HTML for the user input page is saved in add_info.html. In between {% block main %} and {% endblock %}, you can see the code used to display the Add Info form. Most code is HTML, although we employed Jinja to display the drop-down menu options for cohorts that users can select from, since there is a finite list of cohorts to choose from. (List of cohorts stored in lines 23-47 of application.py.)
SOM_network.html and lines 136-137 of application.py feature the code used to display the results of user input from the Add Info page. SOM_Network.html uses HTML to display the table headers and Jinja to loop through the SQL table rows and display data from each row.

Quiz

This page uses the same layout as all the other pages on the site by using Jinja to pull in the layout.html code and injecting it into quiz.html.
The “container” section of this page contains the quiz.
The data in the quiz changes each time the page is refreshed because it runs the quiz SQL query again. This “person” query randomly pulls a single row from the “network” table for which the user will be quizzed on. This query can be found in lines 137 to 142 of application.py.
The Name column is displayed using HTML and Jinja to pull it from the Python list (line 15).
There are four inputs in the quiz: cohort, hometown, past industry, and goal industry. These all have a name equal to their column in the “person” query (lines 17-20).
The “Check Answer” button (line 21) runs the Check function in the JavaScript (lines 50-83). It checks the answers by pulling the Jinja in the name attribute in the input tags, which is converted to HTML, into an if then function in JavaScript. It checks this answer with the user input and the input box turns green if the answer is correct and red if the answer is incorrect. The checking process was made not case sensitive by using the toUpperCase() script.
The user may also choose to see the correct answers by clicking the Display Answers button (line 22). Pressing this button unhides a table that contains the answers for that quiz form (lines 24-41). It does this through a JavaScript function that hides the table until the Display Answers button is clicked on (lines 86-92).
