"""
BaseTest

This class should be the parent class to each non-unit test.
It allows for instantiation of the database dynamically
and makes sure that it is a new, blank database each time.
"""

from unittest import TestCase
from REST_api2.app import app
from REST_api2.db import db


class BaseTest(TestCase):
    # executed prior to each test class
    @classmethod
    def setUpClass(cls):
        # Define a database
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'
        with app.app_context():
            db.init_app(app)
            app.config['DEBUG'] = False
            app.config['PROPAGATE_EXCEPTIONS'] = True

    # executed prior to each test
    def setUp(self):
        with app.app_context():
            db.create_all()
        # Get a test client
        self.app = app.test_client
        self.app_context = app.app_context

    def tearDown(self):
        # Database is blank
        with app.app_context():
            db.session.remove()
            db.drop_all()
