from REST_api2.models.user import UserModel
from REST_api2.tests.unit.unit_basetest import UnitBaseTest


class TestUser(UnitBaseTest):
    def test_create_user(self):
        user = UserModel("test_username", "test_password")
        self.assertEqual(user.username, "test_username")
        self.assertEqual(user.password, "test_password")
