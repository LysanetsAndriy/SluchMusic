import pandas as pd
from extensions import db, api
from models import Genre


def load_genres_from_csv(file_path):
    # Read the CSV file into a DataFrame
    genres_df = pd.read_csv(file_path)

    # Iterate over the DataFrame rows and add each genre to the database
    for index, row in genres_df.iterrows():
        genre = Genre(id=row['genre_id'], name=row['title'])
        db.session.add(genre)

    db.session.commit()
    print("Genres have been successfully added to the database.")


if __name__ == "__main__":
    # Ensure the application context is available
    with api.app_context():
        # Path to the CSV file
        file_path = 'genres.csv'
        load_genres_from_csv(file_path)
