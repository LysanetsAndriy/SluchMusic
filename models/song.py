from extensions import db


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'), nullable=False)
    text = db.Column(db.Text, nullable=True)
    uploader_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    upload_time = db.Column(db.DateTime, nullable=False)
    s3_link = db.Column(db.String(255), nullable=False)  # Link to the song on AWS S3
    favourite_by = db.relationship('FavouriteSongs', backref='song', lazy=True)
    playlists = db.relationship('PlaylistSongs', backref='song', lazy=True)
