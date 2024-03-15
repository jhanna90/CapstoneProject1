from flask import Flask
from flask.testing import FlaskClient
from app import app, db
from unittest import TestCase


class TestRoutes(TestCase):

    # Test to make sure the Homepage route returns  a 200 status code and loads correctly.
    def test_homepage_route(self):
        with app.test_client() as client:
            response = client.get("/")
            self.assertEqual(response.status_code, 200)
            # # Adjust this assertion according to your application's template setup
            self.assertIn(
                b"Everything Changed When The Fire Nation Attacked", response.data
            )

    # The info route should return the info template with information from the API.
    def test_show_info_route(self):
        with app.test_client() as client:
            response = client.get("/info")
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Long Ago...", response.data)

    # The characters route should return the characters template with all characters from the database.
    def test_get_characters_route(self):
        with app.test_client() as client:
            response = client.get("/characters")
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"All Characters", response.data)

    # The episodes route should return the episodes template with all episodes from the API.
    def test_show_episodes_route(self):
        with app.test_client() as client:
            response = client.get("/episodes")
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"List of Episodes", response.data)

    # The trivia questions route should return the questions template with 10 randomly selected questions from the database.
    def test_trivia_questions_route(self):
        with app.test_client() as client:
            response = client.get("/questions")
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Trivia Questions!", response.data)

    # The submit_answers route should redirect to the evaluate_answers route.
    def test_submit_answers_route(self):
        with app.test_client() as client:
            response = client.post("/submit_answers")
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.headers["Location"], "/evaluate_answers")
