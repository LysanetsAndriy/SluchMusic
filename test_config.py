import os
import sys

# Add the parent directory to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@localhost/test_sluch_music'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'very_secret_key'
    JWT_TOKEN_LOCATION = ['headers']
    S3_BUCKET = os.getenv('S3_BUCKET')
    S3_KEY = os.getenv('S3_KEY')
    S3_SECRET = os.getenv('S3_SECRET')
    S3_LOCATION = f"http://{os.getenv('S3_BUCKET')}.s3.amazonaws.com/"
