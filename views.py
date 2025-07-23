from utils.templating import render_template
from router import route

@route("/", methods=["GET"])
def home(environ):
    return render_template("index.html", {"name":"Bozhidar"})