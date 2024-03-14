from flask import Flask
from models import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///avatar_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.secret_key = "shhh secret"

# Initialize the SQLAlchemy 'db' instance with the Flask app
db.init_app(app)

# Import your routes after creating the app instance
from routes import *

if __name__ == "__main__":
    app.run(debug=True)
