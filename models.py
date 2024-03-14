from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_bcrypt import Bcrypt


db = SQLAlchemy()

bcrypt = Bcrypt()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(300), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)
    email = db.Column(db.String(300), unique=True, nullable=False)
    favorite_character = db.Column(db.String(300))

    @classmethod
    def register(cls, username, pwd):
        """Register user w/hashed password & return user."""

        hashed = bcrypt.generate_password_hash(pwd)
        # turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")

        # return instance of user w/username and hashed pwd
        return cls(username=username, password=hashed_utf8)

    # end_register

    # start_authenticate
    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, pwd):
            # return user instance
            return u
        else:
            return False

    # end_authenticate


# Define the Info table
class Info(db.Model):
    """This class represents the Information table about the show"""

    __tablename__ = "info"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    synopsis = db.Column(db.Text, nullable=False)
    years_aired = db.Column(db.String(100), nullable=False)
    genres = db.Column(db.String(200), nullable=False)
    creators = db.Column(db.String(500))

    def make_info_dict(self):
        """Serialzes information into a dictionary so that it can be jsonified"""

        return {
            "id": self.id,
            "synopsis": self.synopsis,
            "yearsAired": self.yearsAired,
            "genres": self.genres,
            "creators": self.creators,
        }


# Define the Characters table
class Characters(db.Model):
    __tablename__ = "characters"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    image = db.Column(db.String(255))
    bio_nationality = db.Column(
        db.String(255)
    )  # Update column name to match the one in your PostgreSQL table
    bio_ethnicity = db.Column(
        db.String(255)
    )  # Update column name to match the one in your PostgreSQL table
    bio_ages = db.Column(
        db.String(255)
    )  # Update column name to match the one in your PostgreSQL table
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


# Define the Episodes table
class Episodes(db.Model):
    __tablename__ = "episodes"
    id = db.Column(db.Integer, primary_key=True)
    season = db.Column(db.Text)
    num_in_season = db.Column(db.Text)
    title = db.Column(db.Text)
    directed_by = db.Column(db.Text)
    original_air_date = db.Column(db.Text)

    def make_episodes_dict(self):
        """Serialzes information into a dictionary so that it can be jsonified"""

        return {
            "id": self.id,
            "season": self.season,
            "num_in_season": self.num_in_season,
            "title": self.title,
            "directed_by": self.directed_by,
            "original_air_date": self.original_air_date,
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
            "possible_answer": self.possible_answers,
            "correct_answer": self.correct_answer,
        }
