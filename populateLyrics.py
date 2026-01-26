import requests
import time
from dotenv import load_dotenv
import os

start_time = time.time()

load_dotenv()
api_key = os.getenv("API_KEY")

mbids = ["31a52323-6da9-43fb-a62b-f389030be585"]
# mbids = ["ef965d09-ff13-4ae4-9514-414a6ec13d3e", "1bc6d800-30a4-4962-99ea-cf0440ed1aa0", "8baa02b6-7956-4edd-a004-1d3cd8941a79", "2082dfe1-fc3c-40d8-8906-6961b0db124e", "31a52323-6da9-43fb-a62b-f389030be585"]

songs = []

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
    album = response.json()["album"]["name"]
    for track in tracks:
        if not any(song[0] == track["name"] for song in songs):
            songs.append((track["name"], "Noah Kahan", album, track["duration"]))

print("Populating lyrics...")
for song in songs:
    response = requests.get(
        "https://lrclib.net/api/get",
        params={
            "track_name": song[0],
            "artist_name": song[1],
            "album_name": song[2],
            "duration": song[3]
        }
    )
    data = response.json()
    if "statusCode" in data:
        if data["statusCode"] == 404:
            print("Lyrics not found for: "+song[0])
    else:
        lyrics = data["plainLyrics"]
        with open("lyrics/"+song[0]+".txt", "w", encoding="utf-8") as f:
            f.write(lyrics)

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