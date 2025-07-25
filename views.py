from utils.templating import render_template
from utils.db import execute_query
from utils.captcha import generate_captcha
import http.cookies
from router import route
import hashlib


@route("/", methods=["GET"])
def home(environ):
    cookies = http.cookies.SimpleCookie(environ.get("HTTP_COOKIE", ""))
    email_cookie = cookies.get("email")
    if email_cookie:
        email = email_cookie.value
        user = execute_query(
            "SELECT first_name FROM users WHERE email = %s", (email,),fetchone=True
        )
        if user:
           return render_template("index.html", {"name": user[0]})
    return render_template("index.html")

@route("/register", methods=['GET','POST'])
def register(environ):
    cookies = http.cookies.SimpleCookie(environ.get("HTTP_COOKIE", ""))
    if cookies.get("email"):
        return "REDIRECT:/"
    if environ["REQUEST_METHOD"] == "POST":
        try:
            size = int(environ.get("CONTENT_LENGTH", 0))
        except ValueError:
            size = 0
        body = environ["wsgi.input"].read(size).decode()
        params = dict(x.split("=") for x in body.split("&"))
        email = params.get("email")
        first_name = params.get("first_name")
        last_name = params.get("last_name")
        password = params.get("password")
        confirm = params.get("confirm")
        captcha_answer = params.get("captcha_answer")
        captcha_expected = params.get("captcha_expected")

        if not email or not first_name or not last_name or not password or password != confirm:
            question,expected = generate_captcha()
            return render_template("register.html", {"error": "invalid input",
                    "captcha_question": question,
                    "captcha_expected": expected})
        if captcha_answer !=  captcha_expected:
            question,expected = generate_captcha()
            return render_template("register.html", {"error": "Wrong captcha",
                    "captcha_question": question,
                    "captcha_expected": expected})
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        try:
            execute_query(
                "INSERT INTO users (email,first_name,last_name,password_hash) VALUES (%s,%s,%s,%s)",
                (email,first_name,last_name,password_hash)
            )
            return "REDIRECT:/login"
        except Exception as e:
            question,expected = generate_captcha()
            return render_template("register.html", {"error": "User already exists or DB error",
                    "captcha_question": question,
                    "captcha_expected": expected})
    else:
        question,expected = generate_captcha()
        return render_template("register.html", {"captcha_question": question,
                    "captcha_expected": expected})

@route("/login",methods=["GET","POST"])
def login(environ):
    cookies = http.cookies.SimpleCookie(environ.get("HTTP_COOKIE", ""))
    if cookies.get("email"):
        return "REDIRECT:/"
    if environ["REQUEST_METHOD"] == "POST":
        try:
            size = int(environ.get("CONTENT_LENGTH", 0))
        except ValueError:
            size = 0
        body = environ["wsgi.input"].read(size).decode()
        params = dict(x.split("=") for x in body.split("&"))
        email = params.get("email")
        password = params.get("password")
        captcha_answer = params.get("captcha_answer")
        captcha_expected = params.get("captcha_expected")
        if not email or not password:
            question,expected = generate_captcha()
            return render_template("login.html", {"error": "invalid input","captcha_question":question,"captcha_expected":expected})
        
        if captcha_answer != captcha_expected:
            question,expected = generate_captcha()
            return render_template("login.html", {"error": "invalid captcha","captcha_question":question,"captcha_expected":expected})

        password_hash = hashlib.sha256(password.encode()).hexdigest()
        user = execute_query(
            "SELECT * FROM users WHERE email=%s AND password_hash=%s",
            (email,password_hash),
            fetchone=True
        )
        if user:
            environ["set_cookie"] = f"email={email}; Path=/"
            return "REDIRECT:/"
        else:
            question,expected = generate_captcha()
            return render_template("login.html", {"error": "invalid username or password","captcha_question":question,"captcha_expected":expected})
    else:
        question,expected = generate_captcha()
        return render_template("login.html",{"captcha_question":question,"captcha_expected":expected})

@route("/logout",methods=["GET"])
def logout(environ):
    environ["set_cookie"] = "email=; Path=/; Expires=Thu, 01 Jan 1970 00:00:00 GMT"
    return "REDIRECT:/"