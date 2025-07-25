import unittest
from server import app
from router import route_table
from utils.templating import render_template
from io import BytesIO

class TestRouterAndServer(unittest.TestCase):
    def setUp(self):
        self.environ_base = {
            'wsgi.input': BytesIO(),
            'CONTENT_LENGTH': 0,
            'SERVER_NAME': 'localhost',
            'SERVER_PORT': '8000',
            'wsgi.url_scheme': 'http',
        }

    def start_response(self,status,headers):
        self.status = status
        self.headers = headers
    

    def test_route_registration(self):
        self.assertIn('/',route_table)
        self.assertIn('GET',route_table['/'])
        self.assertIn("/register",route_table)
        self.assertIn("GET",route_table["/register"])
        self.assertIn("/login",route_table)
        self.assertIn("GET",route_table["/login"])
        self.assertIn("/logout",route_table)
        self.assertIn("GET",route_table["/logout"])
        self.assertIn("/change-name",route_table)
        self.assertIn("GET",route_table["/change-name"])
        self.assertIn("/change-password",route_table)
        self.assertIn("GET",route_table["/change-password"])

    def test_get_home(self):
        environ = self.environ_base.copy()
        environ["PATH_INFO"] = "/"
        environ["REQUEST_METHOD"] = "GET"
        result = app(environ,self.start_response)
        self.assertEqual(self.status,"200 OK")
    
    def test_get_register(self):
        environ = self.environ_base.copy()
        environ["PATH_INFO"] = "/register"
        environ["REQUEST_METHOD"] = "GET"
        result = app(environ,self.start_response)
        self.assertEqual(self.status,"200 OK")
        self.assertTrue(any(b"Register" in part for part in result))

    def test_get_login(self):
        environ = self.environ_base.copy()
        environ["PATH_INFO"] = "/login"
        environ["REQUEST_METHOD"] = "GET"
        result = app(environ,self.start_response)
        self.assertEqual(self.status,"200 OK")
        self.assertTrue(any(b"Log" in part for part in result))    
         
    
    def test_404(self):
        environ = self.environ_base.copy()
        environ["PATH_INFO"] = "/notfound"
        environ["REQUEST_METHOD"] = "GET"
        result = app(environ,self.start_response)
        self.assertTrue(any(b'404' in part for part in result))

if __name__ == '__main__':
    unittest.main()