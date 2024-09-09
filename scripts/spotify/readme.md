# Summary

This script is a simple example of how to use the Spotify API to get the top tracks of an artist. It uses the `requests` library to make a GET request to the Spotify API and returns the top tracks of the artist.

In order to use your personal data, you need to request your data to Spotify. You can do it going to your profile, then, to privacy settings, and then, to the "Download your data" section. You will receive a JSON file with all your data. You need to look for the `StreamingHistory_music_0.json` file and put it in the same directory as the script. The script will read the file and return the top tracks of the artist you choose.
# Steps

First, you need to create a Spotify Developer account and create a new app. You will get a client ID and a client secret that you will use to authenticate your requests.
Here's the URL to create a new app: [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications).


Next, you need to populate the `.env` file with your client ID and client secret.

```bash
CLIENT_ID=your_client_id
CLIENT_SECRET=your_client_secret
```

Then, you need to install the script dependencies by running:

```bash
pip install -r requirements.txt
```

Then you need to run the scripts one by one, make sure you have the `StreamingHistory_music_0.json` file in the same directory as the script.

The first script `01_extract_artists.ipynb` is a Jupiter notebook to create the `streaming.csv` file. You need to run the cells one by one to create the file.

The second script `02_artists_obtain_more_data.py` is a Python script that reads the `streaming.csv` file and creates a `artists_data.csv`, a `genres.csv` and a `artists_genres.csv` files. For this
step you will be calling the Spotify API to get more data about the artists.

The third script `03_streaming_improve_data.py` will read the `streaming.csv` file and the `artists_data.csv` file and will create a `streaming_with_artist_id.csv` file. This file will have the artist ID for each track.
if the artist is not found in the `artists_data.csv` file, it will be ignored.

