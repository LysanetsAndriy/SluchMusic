from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

api = Flask(__name__)

# Database Configuration
api.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/sluch_music'
api.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# JWT Configuration
api.config['JWT_SECRET_KEY'] = 'very_secret_key'
api.config['JWT_TOKEN_LOCATION'] = ['headers']

# AWS S3 Configuration
api.config['S3_BUCKET'] = os.getenv('S3_BUCKET')
api.config['S3_KEY'] = os.getenv('S3_KEY')
api.config['S3_SECRET'] = os.getenv('S3_SECRET')
api.config['S3_LOCATION'] = f"http://{api.config['S3_BUCKET']}.s3.amazonaws.com/"

db = SQLAlchemy(api)
migrate = Migrate(api, db)
jwt = JWTManager(api)

