from router import route_table
import views

def app(environ, start_response):
    path = environ.get("PATH_INFO", "/")
    method = environ.get("REQUEST_METHOD", "GET")

    if path in route_table and method in route_table[path]:
        response_body = route_table[path][method](environ)
        if isinstance(response_body,str) and response_body.startswith("REDIRECT:"):
            location = response_body.split(":",1)[1]
            response_headers = []
            if 'set_cookie' in environ:
                response_headers.append(("Set-Cookie", environ['set_cookie']))
            response_headers.append(("Location", location))
            start_response("302 Found", response_headers)
            return[b""]
        status = "200 OK"
    else:
        response_body = [b"404 Not Found"]
        status = "404 Not Found"

    body_length = sum(len(part) for part in response_body)
    response_headers = [
        ("Content-Type", "text/html"),
        ("Content-Length", str(body_length))
    ]
    if 'set_cookie' in environ:
        response_headers.append(("Set-Cookie", environ['set_cookie']))
    start_response(status, response_headers)
    return response_body
