from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)
app.config.from_object('test_config.TestConfig')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        migrate.init_app(app, db)
