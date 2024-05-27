import sys
import os
import pytest
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import api as app, db
from models import User, Song, Genre

# Use the test configuration
app.config.from_object('test_config.TestConfig')

@pytest.fixture(scope='module')
def test_client():
    testing_client = app.test_client()

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    yield testing_client

    ctx.pop()

@pytest.fixture(scope='module')
def init_database():
    # Create the database and the database table(s)
    db.create_all()

    # Insert initial data
    genre = Genre(name="test_genre")
    db.session.add(genre)
    db.session.commit()

    yield db

    db.drop_all()

def test_register(test_client, init_database):
    response = test_client.post('/register', json={
        'name': 'John',
        'surname': 'Doe',
        'nickname': 'JohnDoe',
        'email': 'john@gmail.com',
        'password': '12345678'
    })
    assert response.status_code == 201
    assert b'User registered successfully' in response.data

def test_login(test_client, init_database):
    response = test_client.post('/login', json={
        'email': 'john@gmail.com',
        'password': '12345678'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert 'access_token' in data

def test_protected(test_client, init_database):
    login_response = test_client.post('/login', json={
        'email': 'john@gmail.com',
        'password': '12345678'
    })
    token = login_response.get_json()['access_token']

    response = test_client.get('/protected', headers={
        'Authorization': f'Bearer {token}'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['logged_in_as'] == 'john@gmail.com'

def test_upload_song(test_client, init_database):
    login_response = test_client.post('/login', json={
        'email': 'john@gmail.com',
        'password': '12345678'
    })
    token = login_response.get_json()['access_token']

    with open('Never Gonna Give You Up short.mp3', 'rb') as file:
        response = test_client.post('/upload', headers={
            'Authorization': f'Bearer {token}'
        }, data={
            'file': file
        }, content_type='multipart/form-data')

    assert response.status_code == 201
    data = response.get_json()
    assert 'File successfully uploaded' in data['message']

def test_download_song(test_client, init_database):
    login_response = test_client.post('/login', json={
        'email': 'john@gmail.com',
        'password': '12345678'
    })
    token = login_response.get_json()['access_token']

    # Assume a song with ID 1 exists in the database
    response = test_client.get('/download/1', headers={
        'Authorization': f'Bearer {token}'
    })

    assert response.status_code == 200
    assert 'attachment' in response.headers['Content-Disposition']
