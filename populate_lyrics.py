import requests
import time
from dotenv import load_dotenv
import os
import json
import time
import re
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import requests

start_time = time.time()

def create_session():
    retry_strategy = Retry(
        total=5,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session = requests.Session()
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session

session = create_session()

load_dotenv()
api_key = os.getenv("API_KEY")

# mbids = ["31a52323-6da9-43fb-a62b-f389030be585"]
mbids = ["ef965d09-ff13-4ae4-9514-414a6ec13d3e", "1bc6d800-30a4-4962-99ea-cf0440ed1aa0", "8baa02b6-7956-4edd-a004-1d3cd8941a79", "2082dfe1-fc3c-40d8-8906-6961b0db124e", "31a52323-6da9-43fb-a62b-f389030be585"]

songs = []
albums = []

MANIFEST_FILE = "song-list.json"
LYRICS_ROOT = "lyrics"

def sanitize_filename(name):
    return re.sub(r'[<>:"/\\|?*]', '', name).strip()

print("Gathering songs...")
for id in mbids:
    response = requests.get(
        "https://ws.audioscrobbler.com/2.0/?method=album.getInfo",
        params={
            "mbid": id,
            "api_key": api_key,
            "format": "json"
        }
    )
    tracks = response.json()["album"]["tracks"]["track"]
    album = sanitize_filename(response.json()["album"]["name"])
    if not any(a == album for a in albums):
        albums.append(album)
        album_dir = os.path.join(LYRICS_ROOT, album)
        os.makedirs(album_dir, exist_ok=True)
    for track in tracks:
        if not any(song[0] == track["name"] for song in songs):
            songs.append((track["name"], "Noah Kahan", album, track["duration"]))

print("Populating lyrics...")

with open(MANIFEST_FILE, "w") as f:
    json.dump([], f)

def append_json(item, filename="song-list.json"):
    if not os.path.exists(filename):
        data = []
    else:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
    data.append(item)
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

for song in songs:
    params={
            "artist_name": song[1],
            "track_name": song[0],
            "album_name": song[2],
            "duration": song[3]
        }
    print(params)
    try: 
        response = session.get(
            "https://lrclib.net/api/get",
            params={
                "artist_name": song[1],
                "track_name": song[0],
                "album_name": song[2],
                "duration": song[3]
            }
        )
        data = response.json()
    except requests.exceptions.RequestException as e:
        print("Request failed for "+song[0])
        continue
    if "statusCode" in data:
        if data["statusCode"] == 404:
            print("Lyrics not found for: "+song[0])
    else:
        lyrics = data["plainLyrics"]
        album_dir = os.path.join(LYRICS_ROOT, sanitize_filename(song[2]))
        file_path = os.path.join(album_dir, f"{song[0]}.txt")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(lyrics)
        manifest_entry = {
            "title": song[0],
            "album": song[2],
            "file": file_path.replace("\\", "/")
        }
        append_json(manifest_entry)
    time.sleep(0.5)

end_time = time.time()
runtime = end_time - start_time
print("Songs Fetched: "+str(len(songs)))
print(f"Runtime: {runtime:.4f} seconds")

# response = requests.get(
#     "https://ws.audioscrobbler.com/2.0/?method=artist.getTopAlbums",
#     params={
#         "artist": "Noah Kahan",
#         "api_key": api_key,
#         "format": "json"
#     }
# )

# print(json.dumps(response.json(), indent=4))


# response = requests.get(
#     "https://ws.audioscrobbler.com/2.0/?method=track.getInfo",
#     params={
#         "api_key": api_key,
#         "artist": "Noah Kahan",
#         "track": "Stick Season",
#         "format": "json"
#     }
# )

# num = int(response.json()["track"]["duration"])
# print(num / 1000)


# stick season forever - ef965d09-ff13-4ae4-9514-414a6ec13d3e
# busyhead - 1bc6d800-30a4-4962-99ea-cf0440ed1aa0
# cape elizabeth - 8baa02b6-7956-4edd-a004-1d3cd8941a79
# i was i am - 2082dfe1-fc3c-40d8-8906-6961b0db124e
# hurt somebody - 31a52323-6da9-43fb-a62b-f389030be585