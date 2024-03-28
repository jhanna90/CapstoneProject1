from flask import Flask
from models import db
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL", "postgresql:///avatar_db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.secret_key = "#Avatarthelastairbender!2"
db.init_app(app)
from routes import *

if __name__ == "__main__":
    app.run(debug=True)
