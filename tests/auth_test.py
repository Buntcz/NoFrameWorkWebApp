import unittest
from server import app
from io import BytesIO
import urllib.parse

class TestAuth(unittest.TestCase):
    def setUp(self):
        self.environ_base = {
            'wsgi.input': BytesIO(),
            'CONTENT_LENGTH': 0,
            'SERVER_NAME': 'localhost',
            'SERVER_PORT': '8000',
            'wsgi.url_scheme': 'http',
        }
        self.status = None
        self.headers = None

    def start_response(self, status, headers):
        self.status = status
        self.headers = headers

    def test_register_get(self):
        environ = self.environ_base.copy()
        environ["PATH_INFO"] = "/register"
        environ["REQUEST_METHOD"] = "GET"
        result = app(environ, self.start_response)
        self.assertEqual(self.status, "200 OK")
        self.assertTrue(any(b"Register" in part for part in result))

    def test_register_invalid_input(self):
        environ = self.environ_base.copy()
        environ["PATH_INFO"] = "/register"
        environ["REQUEST_METHOD"] = "POST"
        body = "email=test&first_name=&last_name=&password=123&confirm=123&captcha_answer=5&captcha_expected=5"
        environ["wsgi.input"] = BytesIO(body.encode())
        environ["CONTENT_LENGTH"] = str(len(body))
        result = app(environ, self.start_response)
        self.assertTrue(any(b"invalid input" in part for part in result))

    def test_register_password_mismatch(self):
        environ = self.environ_base.copy()
        environ["PATH_INFO"] = "/register"
        environ["REQUEST_METHOD"] = "POST"
        body = "email=test@test.com&first_name=John&last_name=Doe&password=123&confirm=456&captcha_answer=5&captcha_expected=5"
        environ["wsgi.input"] = BytesIO(body.encode())
        environ["CONTENT_LENGTH"] = str(len(body))
        result = app(environ, self.start_response)
        self.assertTrue(any(b"invalid input" in part for part in result))

    def test_register_wrong_captcha(self):
        environ = self.environ_base.copy()
        environ["PATH_INFO"] = "/register"
        environ["REQUEST_METHOD"] = "POST"
        body = "email=test@test.com&first_name=John&last_name=Doe&password=123&confirm=123&captcha_answer=5&captcha_expected=10"
        environ["wsgi.input"] = BytesIO(body.encode())
        environ["CONTENT_LENGTH"] = str(len(body))
        result = app(environ, self.start_response)
        self.assertTrue(any(b"Wrong captcha" in part for part in result))

    def test_login_get(self):
        environ = self.environ_base.copy()
        environ["PATH_INFO"] = "/login"
        environ["REQUEST_METHOD"] = "GET"
        result = app(environ, self.start_response)
        self.assertEqual(self.status, "200 OK")
        self.assertTrue(any(b"Log" in part for part in result))

    def test_login_invalid_input(self):
        environ = self.environ_base.copy()
        environ["PATH_INFO"] = "/login"
        environ["REQUEST_METHOD"] = "POST"
        body = "email=&password=&captcha_answer=5&captcha_expected=5"
        environ["wsgi.input"] = BytesIO(body.encode())
        environ["CONTENT_LENGTH"] = str(len(body))
        result = app(environ, self.start_response)
        self.assertTrue(any(b"invalid input" in part for part in result))

    def test_login_wrong_captcha(self):
        environ = self.environ_base.copy()
        environ["PATH_INFO"] = "/login"
        environ["REQUEST_METHOD"] = "POST"
        body = "email=test@test.com&password=123&captcha_answer=5&captcha_expected=10"
        environ["wsgi.input"] = BytesIO(body.encode())
        environ["CONTENT_LENGTH"] = str(len(body))
        result = app(environ, self.start_response)
        self.assertTrue(any(b"invalid captcha" in part for part in result))

    def test_login_wrong_credentials(self):
        environ = self.environ_base.copy()
        environ["PATH_INFO"] = "/login"
        environ["REQUEST_METHOD"] = "POST"
        body = "email=nonexistent@test.com&password=wrongpassword&captcha_answer=5&captcha_expected=5"
        environ["wsgi.input"] = BytesIO(body.encode())
        environ["CONTENT_LENGTH"] = str(len(body))
        result = app(environ, self.start_response)
        self.assertTrue(any(b"invalid username or password" in part for part in result))

if __name__ == '__main__':
    unittest.main()