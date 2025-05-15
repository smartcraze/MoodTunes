import os
import random
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

load_dotenv()

client_credentials_manager = SpotifyClientCredentials(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET")
)

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

emotion_to_genre = {
    "happy": "pop",
    "sad": "acoustic",
    "angry": "metal",
    "surprise": "edm",
    "fear": "ambient",
    "neutral": "chill"
}

def get_tracks_by_genre(genre: str):
    results = sp.search(q=f"genre:{genre}", type="track", limit=50)
    all_tracks = results["tracks"]["items"]
    random.shuffle(all_tracks)
    tracks = [
        {
            "name": t["name"],
            "artist": t["artists"][0]["name"],
            "url": t["external_urls"]["spotify"],
            "image": t["album"]["images"][0]["url"] if t["album"]["images"] else None,
            "preview": t["preview_url"]
        }
        for t in all_tracks[:10]
    ]
    return tracks
