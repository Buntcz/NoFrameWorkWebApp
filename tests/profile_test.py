import unittest
from server import app
from io import BytesIO

class TestProfile(unittest.TestCase):
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

    def test_change_name_get_authenticated(self):
        environ = self.environ_base.copy()
        environ["PATH_INFO"] = "/change-name"
        environ["REQUEST_METHOD"] = "GET"
        environ["HTTP_COOKIE"] = "email=test@test.com"
        result = app(environ, self.start_response)
        self.assertEqual(self.status, "200 OK")

    def test_change_name_invalid_input(self):
        environ = self.environ_base.copy()
        environ["PATH_INFO"] = "/change-name"
        environ["REQUEST_METHOD"] = "POST"
        environ["HTTP_COOKIE"] = "email=test@test.com"
        body = "first_name=&last_name="
        environ["wsgi.input"] = BytesIO(body.encode())
        environ["CONTENT_LENGTH"] = str(len(body))
        result = app(environ, self.start_response)
        self.assertTrue(any(b"Invalid input" in part for part in result))

    def test_change_name_missing_first_name(self):
        environ = self.environ_base.copy()
        environ["PATH_INFO"] = "/change-name"
        environ["REQUEST_METHOD"] = "POST"
        environ["HTTP_COOKIE"] = "email=test@test.com"
        body = "first_name=&last_name=Smith"
        environ["wsgi.input"] = BytesIO(body.encode())
        environ["CONTENT_LENGTH"] = str(len(body))
        result = app(environ, self.start_response)
        self.assertTrue(any(b"Invalid input" in part for part in result))

    def test_change_password_get_authenticated(self):
        environ = self.environ_base.copy()
        environ["PATH_INFO"] = "/change-password"
        environ["REQUEST_METHOD"] = "GET"
        environ["HTTP_COOKIE"] = "email=test@test.com"
        result = app(environ, self.start_response)
        self.assertEqual(self.status, "200 OK")

    def test_change_password_invalid_input(self):
        environ = self.environ_base.copy()
        environ["PATH_INFO"] = "/change-password"
        environ["REQUEST_METHOD"] = "POST"
        environ["HTTP_COOKIE"] = "email=test@test.com"
        body = "old_password=&new_password=&confirm="
        environ["wsgi.input"] = BytesIO(body.encode())
        environ["CONTENT_LENGTH"] = str(len(body))
        result = app(environ, self.start_response)
        self.assertTrue(any(b"Invalid Input" in part for part in result))

    def test_change_password_mismatch(self):
        environ = self.environ_base.copy()
        environ["PATH_INFO"] = "/change-password"
        environ["REQUEST_METHOD"] = "POST"
        environ["HTTP_COOKIE"] = "email=test@test.com"
        body = "old_password=oldpass&new_password=newpass&confirm=different"
        environ["wsgi.input"] = BytesIO(body.encode())
        environ["CONTENT_LENGTH"] = str(len(body))
        result = app(environ, self.start_response)
        self.assertTrue(any(b"Invalid Input" in part for part in result))

    def test_change_password_wrong_current(self):
        environ = self.environ_base.copy()
        environ["PATH_INFO"] = "/change-password"
        environ["REQUEST_METHOD"] = "POST"
        environ["HTTP_COOKIE"] = "email=test@test.com"
        body = "old_password=wrongpass&new_password=newpass&confirm=newpass"
        environ["wsgi.input"] = BytesIO(body.encode())
        environ["CONTENT_LENGTH"] = str(len(body))
        result = app(environ, self.start_response)
        self.assertTrue(any(b"Current password is incorrect" in part for part in result))

if __name__ == '__main__':
    unittest.main()