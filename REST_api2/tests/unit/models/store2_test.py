from REST_api2.models.store import StoreModel
from REST_api2.tests.unit.unit_basetest import UnitBaseTest


class StoreTest(UnitBaseTest):
    def test_create_store(self):
        store = StoreModel("test_store")
        self.assertEqual(store.name, "test_store",
                         "The name of the store after creation does not equal the constructor argument.")
