from extensions import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    nickname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)
    role = db.Column(db.String(10), nullable=False)  # 'admin' or 'user'

    favourite_songs = db.relationship('FavouriteSongs', backref='user', lazy=True)
    playlists = db.relationship('Playlist', backref='user', lazy=True)
    uploaded_songs = db.relationship('Song', backref='uploader', lazy=True)
