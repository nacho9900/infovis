import os
import pandas as pd
import spotipy
import uuid
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials
from concurrent.futures import ThreadPoolExecutor, as_completed


def load_env_variables():
    load_dotenv()
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    return client_id, client_secret


def get_spotify_client(client_id, client_secret):
    return spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))


def fetch_artist_data(sp, artist):
    result = sp.search(q=f"artist:{artist}", type="artist")
    if result["artists"]["items"]:
        artist_info = result["artists"]["items"][0]
        # Extract necessary fields
        artist_data = {
            "id": artist_info["id"],
            "name": artist_info["name"],
            "followers": artist_info["followers"]["total"],  # Get followers count
            "popularity": artist_info["popularity"],
            "uri": artist_info["uri"],
            "genres": artist_info["genres"]  # List of genres
        }
        return artist_data
    else:
        print(f"ERROR: Artist {artist} not found")
    return {"name": artist}


def fetch_artists_data(sp, artists, batch_size=5):
    artist_data = []
    with ThreadPoolExecutor(max_workers=batch_size) as executor:
        futures = {executor.submit(fetch_artist_data, sp, artist): artist for artist in artists}
        for count, future in enumerate(as_completed(futures), 1):
            artist = futures[future]
            try:
                data = future.result()
                artist_data.append(data)
                print(f"{count}/{len(artists)}: Retrieved data for {artist}")
            except Exception as e:
                print(f"Error retrieving data for {artist}: {e}")
    return artist_data


def save_data(artist_data, artists_file, genres_file, artists_genres_file):
    print("Saving data to CSV...")
    artist_records = []
    genre_records = {}
    artist_genre_records = []

    for artist in artist_data:
        # Save artist data (id, followers, name, popularity, uri)
        if "id" in artist:
            artist_records.append({
                "id": artist["id"],
                "name": artist["name"],
                "followers": artist["followers"],
                "popularity": artist["popularity"],
                "uri": artist["uri"]
            })

            # Save genres and artist_genre relation
            for genre in artist["genres"]:
                if genre not in genre_records:
                    genre_id = str(uuid.uuid4())
                    genre_records[genre] = genre_id
                else:
                    genre_id = genre_records[genre]

                artist_genre_records.append({
                    "artist_id": artist["id"],
                    "genre_id": genre_id
                })

    # Save to CSV
    pd.DataFrame(artist_records).to_csv(artists_file, index=False)
    pd.DataFrame([{"id": genre_id, "name": genre} for genre, genre_id in genre_records.items()]).to_csv(genres_file, index=False)
    pd.DataFrame(artist_genre_records).to_csv(artists_genres_file, index=False)


def main():
    # Load environment variables
    client_id, client_secret = load_env_variables()

    # Load artist names
    artists = pd.read_csv("../../data/spotify/artists.csv")["name"].tolist()

    # Get Spotify client
    sp = get_spotify_client(client_id, client_secret)

    # Fetch artist data in parallel
    artist_data = fetch_artists_data(sp, artists)

    # Save the data to CSV
    save_data(
        artist_data,
        "../../data/spotify/artists_data.csv",
        "../../data/spotify/genres.csv",
        "../../data/spotify/artists_genres.csv"
    )


if __name__ == "__main__":
    main()
