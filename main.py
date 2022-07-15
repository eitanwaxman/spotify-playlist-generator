import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

env_client_id = os.getenv('SPOTIPY_CLIENT_ID')
env_client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
env_redirect_uri = os.getenv('SPOTIPY_REDIRECT_URI')
scope = "playlist-modify-public"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=env_client_id, client_secret=env_client_secret, redirect_uri=env_redirect_uri, scope=scope))
user_id = sp.current_user()["id"]

date = input("Enter a date in the following format: year-month-day (ex: 2000-08-19)\n")
url = f"https://www.billboard.com/charts/hot-100/{date}"

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

print("getting song titles")

title_elements = soup.select("li > ul > li > h3")
titles = [title.get_text(strip=True) for title in title_elements]
track_uris = []

print("getting track uris")
for title in titles:
    track = sp.search(title, limit=1, offset=0, type="track", market=None)
    try:
        track_uri = track["tracks"]["items"][0]["uri"]
        track_uris.append(track_uri)
        print(title, track_uri)
    except IndexError:
        print(f"index error for:{title}")

print("creating playlist")
new_playlist = sp.user_playlist_create(user_id, f"Top 100 songs from {date}", public=True, description=f"Top 100 songs from {date}")
print(new_playlist["id"])

print("populating playlist")
final_playlist = sp.playlist_add_items(new_playlist["id"], track_uris, position=None)
print(final_playlist)