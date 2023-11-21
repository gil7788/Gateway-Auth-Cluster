import unittest

from main import app
from fastapi.testclient import TestClient


class TestApp(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_root(self):
        response = self.client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Hello World"}

    def test_hello(self):
        response = self.client.get("/hello/John")
        assert response.status_code == 200
        assert response.json() == {"message": "Hello John"}


if __name__ == '__main__':
    unittest.main()
