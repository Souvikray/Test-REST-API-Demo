from REST_api2.models.user import UserModel
from REST_api2.tests.basetest import BaseTest
import json


class UserTest(BaseTest):
    def test_register_user(self):
        with self.app() as client:
            with self.app_context():
                response = client.post('/register', data={'username': "test_username", 'password': "test_password"})
                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(UserModel.find_by_username("test_username"))
                self.assertDictEqual({"message": "User created successfully"}, json.loads(response.data))

    def test_register_and_login(self):
        with self.app() as client:
            with self.app_context():
                client.post('/register', data={'username': "test_username", 'password': "test_password"})
                auth_response = client.post("/auth", data=json.dumps({"username": "test_username", "password": "test_password"}),
                                            headers={"Content-Type": "application/json"})
                self.assertIn("access_token", json.loads(auth_response.data).keys())

    def test_register_duplicate_user(self):
        with self.app() as client:
            with self.app_context():
                client.post('/register', data={'username': "test_username", 'password': "test_password"})
                response = client.post('/register', data={'username': "test_username", 'password': "test_password"})
                self.assertEqual(response.status_code, 400)
                self.assertDictEqual({"message": "A user with that name already exists"}, json.loads(response.data))
