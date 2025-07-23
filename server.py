from router import route_table
import views

def app(environ, start_response):
    path = environ.get("PATH_INFO", "/")
    method = environ.get("REQUEST_METHOD", "GET")

    if path in route_table and method in route_table[path]:
        response_body = route_table[path][method](environ)
        status = "200 OK"
    else:
        response_body = [b"404 Not Found"]
        status = "404 Not Found"

    body_length = sum(len(part) for part in response_body)
    response_headers = [
        ("Content-Type", "text/html"),
        ("Content-Length", str(body_length))
    ]

    start_response(status, response_headers)
    return response_body
