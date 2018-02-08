from REST_api2.models.item import ItemModel
from REST_api2.tests.basetest import BaseTest
from REST_api2.models.store import StoreModel


class ItemTest(BaseTest):
    # test to ensure the database operations are performed correctly
    def test_crud(self):
        with self.app_context():
            StoreModel("test").save_to_db()
            item = ItemModel('test', 19.99, 1)

            self.assertIsNone(ItemModel.find_by_name('test'),
                              "Found an item with name {}, but expected not to.".format(item.name))

            item.save_to_db()

            self.assertIsNotNone(ItemModel.find_by_name('test'))

            item.delete_from_db()

            self.assertIsNone(ItemModel.find_by_name('test'))

    # test to ensure the item-store relationship is indeed established
    def test_item_store_relationship(self):
        with self.app_context():
            store = StoreModel("test_store")
            item = ItemModel("test_item", 12.99, 1)

            store.save_to_db()
            item.save_to_db()
            # check if the item indeed belongs to the particular store
            self.assertEqual(item.store.name, "test_store")
