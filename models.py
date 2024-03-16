from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(300), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)
    email = db.Column(db.String(300), unique=True, nullable=False)
    favorite_character = db.Column(db.String(300))

    # Register user password hashing
    @classmethod
    def register(cls, username, pwd):
        """Register user w/hashed password & return user."""

        hashed = bcrypt.generate_password_hash(pwd)
        # turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")

        # return instance of user w/username and hashed pwd
        return cls(username=username, password=hashed_utf8)

    # User authentication
    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """
        u = User.query.filter_by(username=username).first()
        if u and bcrypt.check_password_hash(u.password, pwd):
            return u
        else:
            return False


# Define the Characters table
class Characters(db.Model):
    __tablename__ = "characters"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    image = db.Column(db.String(255))
    bio_nationality = db.Column(db.String(255))
    bio_ethnicity = db.Column(db.String(255))
    bio_ages = db.Column(db.String(255))
    physical_description_gender = db.Column(db.String(255))
    personal_information_allies = db.Column(db.String(255))
    personal_information_enemies = db.Column(db.String(255))
    personal_information_weapons_of_choice = db.Column(db.String(255))
    personal_information_fighting_styles = db.Column(db.String(255))

    def make_characters_dict(self):
        """Serialzes information into a dictionary so that it can be jsonified"""

        return {
            "id": self.id,
            "name": self.name,
            "image": self.image,
            "bio_nationality": self.bio_nationality,
            "bio_ethnicity": self.bio_ethnicity,
            "bio_ages": self.bio_ages,
            "physical_description_gender": self.physical_description_gender,
            "personal_information_allies": self.personal_information_allies,
            "personal_information_enemies": self.personal_information_enemies,
            "personal_information_weapons_of_choice": self.personal_information_weapons_of_choice,
            "personal_information_fighting_styles": self.personal_information_fighting_styles,
        }


# Define the Questions table
class Questions(db.Model):
    __tablename__ = "questions"
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text)
    possible_answers = db.Column(db.JSON)
    correct_answer = db.Column(db.Text)

    def make_questions_dict(self):
        """Serialzes information into a dictionary so that it can be jsonified"""

        return {
            "id": self.id,
            "question": self.question,
            "possible_answers": self.possible_answers,
            "correct_answer": self.correct_answer,
        }
