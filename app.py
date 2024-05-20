from flask import Flask, jsonify, request, send_file
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import re
from s3_upload import upload_file_to_s3
from s3_download import download_file_from_s3
from datetime import datetime as dt
from mutagen.easyid3 import EasyID3

from extensions import api, db, migrate, jwt

# Import models
from models import User, Song, Genre, FavouriteSongs, Playlist, PlaylistSongs


@api.route("/")
def home():
    return jsonify(
        {
            "message1": "Taranukha Pituh",
            "message2": "Taranukha Chort",
            "message3": "Taranukha Pidr"
        }
    )


@api.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"message": "Missing required fields"}), 400

    name = data.get('name')
    surname = data.get('surname')
    nickname = data.get('nickname')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'user')  # default role is 'user'

    if not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email):
        return jsonify({"error": "Invalid email format"}), 400

    if User.query.filter_by(nickname=nickname).first():
        return jsonify({"error": "User with this nickname already exists"}), 409

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "User with this email already exists"}), 409

    # Hash the password
    hashed_password = generate_password_hash(password)

    new_user = User(
        name=name,
        surname=surname,
        nickname=nickname,
        email=email,
        password=hashed_password,
        role=role
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


@api.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"message": "Missing required fields"}), 400

    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"message": "Invalid credentials"}), 401

    access_token = create_access_token(identity=user.email)
    return jsonify(access_token=access_token), 200


@api.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user_email = get_jwt_identity()
    current_user = User.query.filter_by(email=current_user_email).first()
    return jsonify(logged_in_as=current_user.email), 200


def get_mp3_metadata(file_path):
    try:
        audio = EasyID3(file_path)
        author = audio.get('artist', ['Unknown'])[0]
        return author
    except Exception as e:
        print(f"Error extracting metadata: {e}")
        return 'Unknown'


@api.route("/upload", methods=["POST"])
@jwt_required()
def upload():
    if "file" not in request.files:
        return jsonify({"message": "No file part in the request"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"message": "No file selected for uploading"}), 400

    if file:
        user_email = get_jwt_identity()
        user = User.query.filter_by(email=user_email).first()

        # Save the file temporarily to extract metadata
        temp_file_path = f"/tmp/{file.filename}"
        file.save(temp_file_path)

        # Extract author from metadata
        author = get_mp3_metadata(temp_file_path)
        song = Song.query.filter_by(name=file.filename, author=author).first()
        if song:
            return jsonify({"message": "Song already exists"}), 409

        # Upload file to S3
        s3_url = upload_file_to_s3(temp_file_path, file.filename, file.content_type, api.config["S3_BUCKET"])

        # Save song details to the database
        new_song = Song(
            name=file.filename,
            author=author,
            genre_id=10,
            text="",
            uploader_id=user.id,
            upload_time=dt.utcnow(),
            s3_link=s3_url
        )
        db.session.add(new_song)
        db.session.commit()

        return jsonify({"message": "File successfully uploaded", "url": s3_url}), 201


@api.route("/download/<int:song_id>", methods=["GET"])
@jwt_required()
def download(song_id):
    song = Song.query.get(song_id)
    if not song:
        return jsonify({"message": "Song not found"}), 404

    file_key = song.name
    download_path = download_file_from_s3(file_key, api.config["S3_BUCKET"])

    if not download_path:
        return jsonify({"message": "Failed to download the song"}), 500

    return send_file(download_path, as_attachment=True)


if __name__ == "__main__":
    api.secret_key = 'secret123'
    api.run(debug=True, host="0.0.0.0", port=8080)
