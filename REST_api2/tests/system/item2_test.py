import json
from REST_api2.models.item import ItemModel
from REST_api2.models.store import StoreModel
from REST_api2.models.user import UserModel
from REST_api2.tests.basetest import BaseTest


class TestItem(BaseTest):
    def setUp(self):
        super(TestItem, self).setUp()
        with self.app() as client:
            with self.app_context():
                # get the JWT token
                UserModel("souvik", "1234").save_to_db()
                auth_response = client.post("/auth", data=json.dumps({"username": "souvik", "password": "1234"}),
                                            headers={"Content-Type": "application/json"})
                auth_token = json.loads(auth_response.data)["access_token"]
                #self.access_token = "JWT {}".format(auth_token)
                self.access_token = f"JWT {auth_token}"

    def test_get_item_no_auth(self):
        with self.app() as client:
            with self.app_context():
                resp = client.get("/item/test_item")
                self.assertEqual(resp.status_code, 401)

    def test_get_item_not_found(self):
        # you must be logged in to figure out whether the item exists or not
        with self.app() as client:
            with self.app_context():
                resp = client.get("/item/test_item", headers={"Authorization": self.access_token})
                self.assertEqual(resp.status_code, 404)

    def test_get_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("test_store")
                ItemModel("test_item", 9.99, 1).save_to_db()
                resp = client.get("/item/test_item", headers={"Authorization": self.access_token})
                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual({"name": "test_item", "price": 9.99}, json.loads(resp.data))

    def test_delete_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("test_store").save_to_db()
                ItemModel("test_item", 9.99, 1).save_to_db()
                resp = client.delete("/item/test_item")
                self.assertDictEqual({"message": "Item deleted"}, json.loads(resp.data))

    def test_create_item(self):
        with self.app() as client:
            with self.app_context():
                client.post("/store/test_store")
                resp = client.post("/item/test_item", data={"price": 9.99, "store_id": 1})
                self.assertEqual(resp.status_code, 201)
                self.assertDictEqual({"name": "test_item", "price": 9.99}, json.loads(resp.data))

    def test_create_duplicate_item(self):
        with self.app() as client:
            with self.app_context():
                client.post("/store/test_store")
                client.post("/item/test_item", data={"price": 9.99, "store_id": 1})
                resp = client.post("/item/test_item", data={"price": 19.99, "store_id": 1})
                self.assertEqual(resp.status_code, 400)
                self.assertDictEqual({'message': "An item with name '{}' already exists.".format("test_item")},
                                     json.loads(resp.data))

    def test_put_item(self):
        with self.app() as client:
            with self.app_context():
                client.post("/store/test_store")
                resp = client.put("/item/test_item", data={"price": 9.99, "store_id": 1})
                self.assertEqual(resp.status_code, 201)
                self.assertEqual(ItemModel.find_by_name("test_item").price, 9.99)
                self.assertDictEqual({"name": "test_item", "price": 9.99}, json.loads(resp.data))

    def test_put_update_item(self):
        with self.app() as client:
            with self.app_context():
                client.post("/store/test_store")
                resp = client.post("/item/test_item", data={"price": 9.99, "store_id": 1})
                self.assertDictEqual({"name": "test_item", "price": 9.99}, json.loads(resp.data))
                resp = client.put("/item/test_item", data={"price": 19.99, "store_id": 1})
                self.assertEqual(ItemModel.find_by_name("test_item").price, 19.99)
                self.assertDictEqual({"name": "test_item", "price": 19.99}, json.loads(resp.data))

    def test_item_list(self):
        with self.app() as client:
            with self.app_context():
                client.post("/store/test_store")
                client.post("/store/test_store2")
                client.put("/item/test_item1", data={"price": 9.99, "store_id": 1})
                client.put("/item/test_item2", data={"price": 19.99, "store_id": 2})
                client.post("/item/test_item3", data={"price": 29.99, "store_id": 1})
                client.post("/item/test_item4", data={"price": 39.99, "store_id": 2})
                resp = client.get("/items")
                self.assertDictEqual({"items": [{"name": "test_item1", "price": 9.99},
                                                {"name": "test_item2", "price": 19.99},
                                                {"name": "test_item3", "price": 29.99},
                                                {"name": "test_item4", "price": 39.99}]}, json.loads(resp.data))
