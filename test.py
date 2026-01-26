import requests

mbids = ["ef965d09-ff13-4ae4-9514-414a6ec13d3e", "1bc6d800-30a4-4962-99ea-cf0440ed1aa0", "8baa02b6-7956-4edd-a004-1d3cd8941a79", "2082dfe1-fc3c-40d8-8906-6961b0db124e", "31a52323-6da9-43fb-a62b-f389030be585"]

song = ["Everywhere, Everything", "Noah Kahan", "Stick Season (Forever)", 257]

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