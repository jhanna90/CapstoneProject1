from unittest import TestCase
from flask import current_app
from app import app
from models import db


class TestApp(TestCase):
    @classmethod
    def setUpClass(cls):
        app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///avatar_db"
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        app.config["TESTING"] = True
        cls.app = app.test_client()
        cls.db = db

        # Establish application context
        cls.ctx = app.app_context()
        cls.ctx.push()

        # Create all tables
        cls.db.create_all()

    @classmethod
    def tearDownClass(cls):
        # Establish application context
        app_ctx = current_app.app_context()
        app_ctx.push()

        # Remove the session
        cls.db.session.remove()

        # Remove application context
        app_ctx.pop()

        # Clean up database
        cls.db.drop_all()

    # Unit Test: Testing if the Flask app is running
    def test_flask_app_running(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)

    # Integration Test: Testing if the app can connect to the database
    def test_database_connection(self):
        with app.app_context():
            self.assertTrue(self.db.engine.connect())

    # Integration Test: Testing if the 'SQLALCHEMY_DATABASE_URI' is set properly
    def test_database_uri_set(self):
        self.assertEqual(
            app.config["SQLALCHEMY_DATABASE_URI"], "postgresql:///avatar_db"
        )

    # Unit Test: Testing if 'SQLALCHEMY_TRACK_MODIFICATIONS' is disabled
    def test_track_modifications_disabled(self):
        self.assertFalse(app.config["SQLALCHEMY_TRACK_MODIFICATIONS"])

    # Unit Test: Testing if 'SQLALCHEMY_ECHO' is enabled
    def test_sqlalchemy_echo_enabled(self):
        self.assertTrue(app.config["SQLALCHEMY_ECHO"])
