import json
from REST_api2.models.store import StoreModel
from REST_api2.models.item import ItemModel
from REST_api2.tests.basetest import BaseTest


class TestStore(BaseTest):
    def test_create_store(self):
        with self.app() as client:
            with self.app_context():
                resp = client.post("/store/test_store")
                self.assertEqual(resp.status_code, 201)
                self.assertIsNotNone(StoreModel.find_by_name("test_store"))
                self.assertDictEqual({"id": 1, "name": "test_store", "items": []}, json.loads(resp.data))

    def test_create_duplicate_store(self):
        with self.app() as client:
            with self.app_context():
                client.post("/store/test_store")
                resp = client.post("/store/test_store")
                self.assertEqual(resp.status_code, 400)
                self.assertDictEqual({"message": "A store with name '{}' already exists.".format("test_store")},
                                     json.loads(resp.data))

    def test_delete_store(self):
        with self.app() as client:
            with self.app_context():
                client.post("/store/test_store")
                resp = client.delete("/store/test_store")
                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual({"message": "Store deleted"}, json.loads(resp.data))

    def test_find_store(self):
        with self.app() as client:
            with self.app_context():
                resp = client.get("/store/test_store")
                self.assertEqual(resp.status_code, 404)
                self.assertDictEqual({"message": "Store not found"}, json.loads(resp.data))

                client.post("/store/test_store")

                resp = client.get("/store/test_store")
                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual({"id": 1, "name": "test_store", "items": []}, json.loads(resp.data))
                self.assertIsNotNone(StoreModel.find_by_name("test_store"))

    def test_store_not_found(self):
        with self.app() as client:
            with self.app_context():
                resp = client.get("/store/test_store")
                self.assertEqual(resp.status_code, 404)
                self.assertDictEqual({"message": "Store not found"}, json.loads(resp.data))

    def test_store_found_with_items(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("test_store").save_to_db()
                ItemModel("test_item", 19.99, 1).save_to_db()
                resp = client.get("/store/test_store")
                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual({"id": 1, "name": "test_store",
                                      "items": [{"name": "test_item", "price": 19.99}]}, json.loads(resp.data))

    def test_store_list(self):
        with self.app() as client:
            with self.app_context():
                client.post("/store/test_store")
                client.post("/store/test_store2")
                resp = client.get("/stores")
                self.assertDictEqual({"stores": [{"id": 1, "name": "test_store", "items": []},
                                                 {"id": 2, "name": "test_store2", "items": []}]}, json.loads(resp.data))

    def test_store_list_with_items(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("test_store").save_to_db()
                StoreModel("test_store2").save_to_db()
                ItemModel("test_item", 19.99, 1).save_to_db()
                ItemModel("test_item2", 9.99, 2).save_to_db()
                resp = client.get("/stores")
                self.assertDictEqual({"stores": [{"id": 1, "name": "test_store", "items": [{"name": "test_item", "price": 19.99}]},
                                                 {"id": 2, "name": "test_store2", "items": [{"name": "test_item2", "price": 9.99}]}]},
                                     json.loads(resp.data))

