from utils.templating import render_template
from utils.db import execute_query
import http.cookies
from router import route
import hashlib

@route("/", methods=["GET"])
def home(environ):
    cookies = http.cookies.SimpleCookie(environ.get("HTTP_COOKIE", ""))
    username = cookies.get("username")
    if username:
        return render_template("index.html", {"name": username.value})
    else:
        return render_template("index.html")

@route("/register", methods=['GET','POST'])
def register(environ):
    cookies = http.cookies.SimpleCookie(environ.get("HTTP_COOKIE", ""))
    if cookies.get("username"):
        return "REDIRECT:/"
    if environ["REQUEST_METHOD"] == "POST":
        try:
            size = int(environ.get("CONTENT_LENGTH", 0))
        except ValueError:
            size = 0
        body = environ["wsgi.input"].read(size).decode()
        params = dict(x.split("=") for x in body.split("&"))
        username = params.get("username")
        password = params.get("password")
        confirm = params.get("confirm")

        if not username or not password or password != confirm:
            return render_template("register.html", {"error": "invalid input"})
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        try:
            execute_query(
                "INSERT INTO users (username,password_hash) VALUES (%s,%s)",
                (username,password_hash)
            )
            return render_template("register.html", {"success": "Registration successful!"})
        except Exception as e:
            return render_template("register.html", {"error": "User already exists or DB error"})
    return render_template("register.html")

@route("/login",methods=["GET","POST"])
def login(environ):
    cookies = http.cookies.SimpleCookie(environ.get("HTTP_COOKIE", ""))
    if cookies.get("username"):
        return "REDIRECT:/"
    if environ["REQUEST_METHOD"] == "POST":
        try:
            size = int(environ.get("CONTENT_LENGTH", 0))
        except ValueError:
            size = 0
        body = environ["wsgi.input"].read(size).decode()
        params = dict(x.split("=") for x in body.split("&"))
        username = params.get("username")
        password = params.get("password")
        if not username or not password:
            return render_template("login.html", {"error": "invalid input"})
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        user = execute_query(
            "SELECT * FROM users WHERE username=%s AND password_hash=%s",
            (username,password_hash),
            fetchone=True
        )
        if user:
            environ["set_cookie"] = f"username={username}; Path=/"
            return "REDIRECT:/"
        else:
            return render_template("login.html", {"error": "invalid username or password"})
    return render_template("login.html")