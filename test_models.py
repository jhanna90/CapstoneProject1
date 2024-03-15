from app import app, db
from models import User, Characters, Questions, connect_db
from unittest import TestCase, mock


class TestCodeUnderTest(TestCase):

    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///avatar_db"
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        cls.app_context = app.app_context()
        cls.app_context.push()
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def setUp(self):
        self.client = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_connect_db(self):
        self.assertTrue("sqlalchemy" in app.extensions)

    def test_register_user(self):
        username = "test_user"
        password = "test_password"
        with mock.patch("models.User.password", return_value=True):
            user = User.register(username, password)
            self.assertTrue(user.password)

    def test_authenticate_user_correct_password(self):
        username = "test_user"
        password = "test_password"

        User.register(username, password)

        user = User.authenticate(username, password)
        self.assertIsNotNone(user)

    def test_authenticate_user_incorrect_password(self):
        username = "test_user"
        password = "test_password"
        wrong_password = "wrong_password"

        User.register(username, password)

        user = User.authenticate(username, wrong_password)
        self.assertEqual(user, False)

    def test_make_questions_dict(self):
        question = Questions(
            question="What is the primary bending style of Aang?",
            possible_answers=["Airbending", "Waterbending"],
            correct_answer="Airbending",
        )
        question_dict = question.make_questions_dict()

        self.assertEqual(
            question_dict["question"], "What is the primary bending style of Aang?"
        )
        self.assertEqual(
            question_dict["possible_answers"], ["Airbending", "Waterbending"]
        )
        self.assertEqual(question_dict["correct_answer"], "Airbending")

    def test_query_nonexistent_user(self):
        user = User.query.filter_by(username="nonexistent_user").first()
        self.assertIsNone(user)

    def test_make_characters_dict(self):
        character = Characters(
            name="Aang",
            image="aang.jpg",
            bio_nationality="Air Nomad",
            bio_ethnicity="Air Nomad",
            bio_ages="112",
            physical_description_gender="Male",
            personal_information_allies="Team Avatar",
            personal_information_enemies="Fire Nation",
            personal_information_weapons_of_choice="Airbending",
            personal_information_fighting_styles="Airbending",
        )
        character_dict = character.make_characters_dict()

        expected_dict = {
            "id": None,
            "name": "Aang",
            "image": "aang.jpg",
            "bio_nationality": "Air Nomad",
            "bio_ethnicity": "Air Nomad",
            "bio_ages": "112",
            "physical_description_gender": "Male",
            "personal_information_allies": "Team Avatar",
            "personal_information_enemies": "Fire Nation",
            "personal_information_weapons_of_choice": "Airbending",
            "personal_information_fighting_styles": "Airbending",
        }

        self.assertEqual(character_dict, expected_dict)

    def test_make_characters_dict_empty_fields(self):
        # Test case with empty fields
        character = Characters(
            name="Aang",
            image="",
            bio_nationality="",
            bio_ethnicity="Air Nomad",
            bio_ages="",
            physical_description_gender="",
            personal_information_allies="",
            personal_information_enemies="Fire Nation",
            personal_information_weapons_of_choice="Airbending",
            personal_information_fighting_styles="",
        )
        character_dict = character.make_characters_dict()

        expected_dict = {
            "id": None,
            "name": "Aang",
            "image": "",
            "bio_nationality": "",
            "bio_ethnicity": "Air Nomad",
            "bio_ages": "",
            "physical_description_gender": "",
            "personal_information_allies": "",
            "personal_information_enemies": "Fire Nation",
            "personal_information_weapons_of_choice": "Airbending",
            "personal_information_fighting_styles": "",
        }

        self.assertEqual(character_dict, expected_dict)

    def test_make_characters_dict_none_fields(self):
        # Test case with None fields
        character = Characters(
            name="Aang",
            image=None,
            bio_nationality=None,
            bio_ethnicity="Air Nomad",
            bio_ages=None,
            physical_description_gender=None,
            personal_information_allies=None,
            personal_information_enemies="Fire Nation",
            personal_information_weapons_of_choice="Airbending",
            personal_information_fighting_styles=None,
        )
        character_dict = character.make_characters_dict()

        expected_dict = {
            "id": None,
            "name": "Aang",
            "image": None,
            "bio_nationality": None,
            "bio_ethnicity": "Air Nomad",
            "bio_ages": None,
            "physical_description_gender": None,
            "personal_information_allies": None,
            "personal_information_enemies": "Fire Nation",
            "personal_information_weapons_of_choice": "Airbending",
            "personal_information_fighting_styles": None,
        }

        self.assertEqual(character_dict, expected_dict)
