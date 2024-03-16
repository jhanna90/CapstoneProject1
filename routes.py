from flask import render_template, request, redirect, url_for, session, jsonify
from app import app
from models import (
    User,
    db,
    Characters,
    Questions,
)
import random
import requests
from flask_bcrypt import bcrypt


@app.route("/")
def homepage():
    return render_template("homepage.html")


# Info route shows basic information about the show.
@app.route("/info", methods=["GET"])
def show_info():
    """Returns all information about the Avatar"""
    # Fetch information from the API
    url = "https://api.sampleapis.com/avatar/info"
    response = requests.get(url)
    if response.status_code == 200:
        info = response.json()
        return render_template("info.html", info=info)
    else:
        return "Failed to fetch information from the API", 500


# Characters route retrieves characters from the database and renders them on the client side.
@app.route("/characters", methods=["GET"])
def get_characters():
    characters = Characters.query.all()
    return render_template("characters.html", characters=characters)


# Episodes route shows a user all the episodes in the series. A filter was added so a user can see each episode per season.
@app.route("/episodes", methods=["GET"])
def show_episodes():
    selected_season = request.args.get("season")
    url = "https://api.sampleapis.com/avatar/episodes"
    response = requests.get(url)
    if response.status_code == 200:
        episodes = response.json()

        # Filter episodes based on the selected season
        if selected_season:
            filtered_episodes = [
                episode for episode in episodes if episode["Season"] == selected_season
            ]
            return render_template(
                "episodes.html",
                episodes=filtered_episodes,
                selected_season=selected_season,
            )
        else:
            return render_template(
                "episodes.html", episodes=episodes, selected_season=None
            )
    else:
        return jsonify({"error": "Failed to fetch episodes"}), 500


@app.route("/questions", methods=["GET"])
def trivia_questions():
    """Returns a list of randomly selected Avatar related questions from the database."""
    try:
        all_questions = Questions.query.all()

        if all_questions:
            # Randomly select 10 questions with correct answers
            selected_questions = random.sample(
                all_questions, min(len(all_questions), 10)
            )
            # Store correct answers in session
            correct_answers = {
                question.id: question.correct_answer for question in selected_questions
            }
            session["correct_answers"] = correct_answers

            return render_template("trivia.html", questions=selected_questions)
        else:
            return jsonify({"error": "No questions found in the database"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Submits quiz answers and saves them to session to be used by the evaluation route
@app.route("/submit_answers", methods=["POST"])
def submit_answers():
    if request.method == "POST":
        submitted_answers = request.form.to_dict()
        session["submitted_answers"] = submitted_answers
        print("Submitted Answers:", session["submitted_answers"])

        return redirect(url_for("evaluate_answers"))


# Evaluates and displays user's answer to trivia quiz
@app.route("/evaluate_answers", methods=["GET"])
def evaluate_answers():
    submitted_answers = session.get("submitted_answers")
    correct_answers = session.get("correct_answers")
    print("Submitted Answers:", submitted_answers)
    print("Correct Answers:", correct_answers)

    if submitted_answers and correct_answers:
        score = 0
        for question_id, submitted_answer in submitted_answers.items():
            question_id = int(question_id)
            question = Questions.query.filter_by(id=question_id).first()
            if question and submitted_answer == question.correct_answer:
                score += 1

        return render_template(
            "triviaResults.html",
            score=score,
            submitted_answers=submitted_answers,
            correct_answers=correct_answers,
        )
    else:
        return render_template(
            "triviaResults.html", score=0, submitted_answers={}, correct_answers={}
        )


# Individual Character Profile Page
@app.route("/character/<int:id>", methods=["GET"])
def get_character(id):
    character = Characters.query.get(id)

    if character:
        return render_template(
            "character.html",
            character=character,
        )
    else:
        return render_template("character.html", character=character)


# Sign-up route
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        favorite_character = request.form.get("favorite_character")
        # Generate salt and hash the password
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)

        # Create a new user object with hashed password
        new_user = User(
            username=username,
            password=hashed_password.decode("utf-8"),
            email=email,
            favorite_character=favorite_character,
        )
        db.session.add(new_user)
        db.session.commit()

        return render_template("signedUp.html", username=username)
    characters = Characters.query.all()

    return render_template("signup.html", characters=characters)


# Login route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username_or_email = request.form["username_or_email"]
        password = request.form["password"]
        user = User.query.filter(
            (User.username == username_or_email) | (User.email == username_or_email)
        ).first()

        if user:
            # Verify the password
            if bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
                session["user_id"] = user.id
                return render_template("loginResult.html", username=user.username)
            else:
                return render_template(
                    "loginResult.html", message="Invalid username/email or password"
                )

    # If the request method is not POST or the login was unsuccessful, render the login form
    return render_template("login.html")


# Logout route
@app.route("/logout", methods=["POST"])
def logout():
    session.pop("user_id", None)
    return render_template("logout.html")
