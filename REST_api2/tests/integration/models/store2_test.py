from REST_api2.models.store import StoreModel
from REST_api2.models.item import ItemModel
from REST_api2.tests.basetest import BaseTest


class StoreTest(BaseTest):
    def test_create_store_items_empty(self):
        store = StoreModel("test_store")
        self.assertEqual(store.items.all(), [],
                         "The store's items list was not empty even though no items were added")

    def test_crud(self):
        with self.app_context():
            store = StoreModel("test_store")
            self.assertIsNone(StoreModel.find_by_name("test_store"))
            store.save_to_db()
            self.assertIsNotNone(StoreModel.find_by_name("test_store"))
            store.delete_from_db()
            self.assertIsNone(StoreModel.find_by_name("test_store"))

    def test_store_item_relationship(self):
        with self.app_context():
            store = StoreModel("test_store")
            item = ItemModel("test_item", 12.99, 1)
            store.save_to_db()
            item.save_to_db()
            self.assertEqual(store.items.count(), 1)
            self.assertEqual(store.items.first().name, "test_item")

    def test_store_json(self):
        store = StoreModel("test_store")
        expected = {"id": None, "name": "test_store", "items": []}
        self.assertDictEqual(expected, store.json())

    def test_store_json_with_item(self):
        with self.app_context():
            store = StoreModel("test_store")
            item = ItemModel("test_item", 12.99, 1)
            store.save_to_db()
            item.save_to_db()
            expected = {"id": 1, "name": "test_store", "items": [{"name": "test_item", "price": 12.99}]}
            self.assertDictEqual(expected, store.json())
