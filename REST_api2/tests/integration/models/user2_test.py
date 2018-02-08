from REST_api2.models.user import UserModel
from REST_api2.tests.basetest import BaseTest


class TestUser(BaseTest):
    def test_crud(self):
        with self.app_context():
            user = UserModel("test_username", "test_password")
            self.assertIsNone(user.find_by_username("test_username"))
            self.assertIsNone(user.find_by_id(1))
            user.save_to_db()
            self.assertIsNotNone(user.find_by_username("test_username"))
            self.assertIsNotNone(user.find_by_id(1))
