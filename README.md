This project is Python Web Auth (login/register/logout/change name/change password) without using any web framework. the only things I used were the random library, http library , unittest, gunicorn and WSGI(Web Server Gateway Interface.)

To be able to see the project in full power you would need to:

1. Create an env. (Run in the file directory after you cloned the repository):
```bash
python3 -m venv .venv
```

2. Activate the environment (Run this again in the terminal):
```bash
source .venv/bin/activate
```

3. Install all the requirements from requirements.txt
```bash
pip install -r requirements.txt
```

4. Make sure you have PostgreSQL downloaded if not download it for linux(Ubuntu based) with this command:
```bash
sudo apt install postgresql
```

5. After that create a db:
```bash
createdb users
```

6. Then run this to create the table for the users using schema.sql
```bash
psql -U postgres -d users -f schema.sql
```
After you run it the table will be ready for use.

7. Then if you wish you can run all the tests
```bash
python -m unittest tests/test_file_name.py
```

8. Your project is ready to be ran using
```bash
gunicorn server:app
```

9. Enjoy
# ATTENTION: The project currently only works on chrome due to using WSGI and not more flexible framework as Chrome or Firefox#

# Functionalities and how I realised them #

## router.py ##
in router.py I recreated the same router used in the all famous framework flask by recreating the route_table which holds all routes and their methods GET,POST. I recreated the functionality to be the same by using a decorateor to take the route and the method used and then to run the function provided under it. Just like flask but not as flexible.

## server.py ##
in the server we are taking the current path and the method that the user wants to use trough the environ(Environ is a dict which holds all the values that are passed into a content-header for a website and I directly manipulate them) after which I use the imported route_table to look for these routes , if they exists the function under the decorator is ran and if not they are sent to a 404 Not Found page. There is also Redirect logic which I added for the login and register. It works so when somebody registers a redirect is sent and if it's a redirect it splits it trough the ":" symbol and takes the second parameter which is the path that need to be redirected sending a 302 Found code. And if all goes well it rans the function decorator and sends a 200 OK code.

## views.py ##
All the views created with the route funcion.


### home view ###
The home view is the standart view it checks if a user is logged in trough environ["HTTP_COOKIE"], we are using the email as a cookie as it's the safest for each user. If there is an email cookie returned we return the index.html template with the 2 names(That we took with SQL query) as context. And if not the index.html is returned asking the user to log in or register.

### register view ###
The register view if user is already logged in redirects to the main page, if not the user is asked for email,first name, last name , password and to confirm his password. If he does all these steps and they are right and he solves the captcha(I put captcha in register for safety reasons if bots want to create accounts) the password is hashed,an SQL query is ran and the account is added into the PostgreSQL database. If there is an error it loads register.html again with the errors displayed.

I am taking the input from the forms trough environ["wsgi.input"] and after that I take the params by splitting them from the "&" and then the "=" saving them into a dictionary so I can use them for SQL query.

### login view ###
The login view checks first if the user is already logged in trough the cookie if he is the user is redirected back to the main page. If not the user can log in using the credentials used in the register and by solving the captcha. After that a query is ran checking if there is an email the same as the provided and if the passwords hashes match. If they do the user is redirected to the index greeting him with the 2 names used to register, if not it loads login again with the error displayed.

I am taking the input from the forms trough environ["wsgi.input"] and after that I take the params by splitting them from the "&" and then the "=" saving them into a dictionary so I can use them for SQL query.

And when the user successfully logs in I set the cookie for the sessio to their e-mail.

### logout view ###
Just clears the cookie by setting it both to a empty one and expired one at the same time for more safety and redirects the user to the main page.

### change name ###
Prompts the user for new first name and new last name after.
I am taking the input from the forms trough environ["wsgi.input"] and after that I take the params by splitting them from the "&" and then the "=" saving them into a dictionary so I can use them for SQL query which updates the names for the current user in the session.

### change password ###
Promps the user for current password, new password and to confirm his new password when he does so an SQL query is ran checking if the old password hash is correct it hashes the new password and updates the database if not the template is rendered with the corresponding error.

I am taking the input from the forms trough environ["wsgi.input"] and after that I take the params by splitting them from the "&" and then the "=" saving them into a dictionary so I can use them for SQL query which updates the names for the current user in the session.

# ATTENTION: #
In almost all views I check if the user is already logged it trough the environ["HTTP_COOKIE"] so I can display different stuff on the page or redirect them. Also in all forms I am using the same method for taking the parameters from the forms using their corresponding html names. And I am using http library to take the cookie using the SimpleCookie class and hashlib to hash the passwords.

## schema.sql ##
Schema for the creation of the user table which has an email,first name,last name the hashed password and created_at to know when the account was created.

## db.by ##
Simple database connection using my credentials for the postgreSQL database (you should use yours not mine to connect). And a function tha executes queries which is the most basic one if there is a connection it tries to run the query with the parameters and then closses the connection if not it just closses it.

## templating.py ##
Simple render_template function I made with the help of jinja2.

## captcha.py ##
Simple math captcha made by using random library to create a random numbers for math equation.

## templates ##
All templates are very basic. Just forms with POST method to them.

## tests ##
All test are passing and I made a test for each functionallity in the project.

## style.css ##
Sorry for the minimal styling I had no time for it because the project was quite hard to grasp.

# TECHNOLOGIES USED: #
#### WSGI(Web Server Gateway Interface),Jinja2,HTML,CSS,Unittest,psycopg2,PostgreSQL,Python Virual Env,Gunicorn,Http,random library. ####

