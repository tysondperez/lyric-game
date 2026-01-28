# Lyric Game

Lyric Game (working title) is a website hosted on GitHub Pages that allows users to guess a song by typing in lyrics. This repo also contains the python file that was used to gather and download the lyrics for all supported songs. 
To play the game, there is no set up required. Simply go to [this link](https://tysondperez.github.io/lyric-game/) to play now!

## Installation
*(Note: installation is required only to run *`populate_lyrics.py`*.)*

To install the lyric downloader, install python [here](https://www.python.org/downloads/), or via the command line of your chosen terminal. All packages used in this program should be included in Python 3.10.12 or later.

This program utilizes the APIs of both [LastFM](https://www.last.fm/api) and [LRCLIB](https://lrclib.net/docs). LRCLIB is openly accessible, but **LastFM requires users to apply for an API key** before their queries are allowed to run. 

Once this is done, simply create a file named `.env` in the same directory as this program to allow you to access the LastFM API.

## Usage
*(Note: Usage is required only to run *`populate_lyrics.py`*.)*

```WSL
python3 populate_lyrics.py
```

At this time, only a select portion of songs from a select artist are supported (shoutout Noah Kahan). As a result, running the program will only search for all songs from the pre-specified albums.

## Future Work

As mentioned above, this project currently supports only 58 selected songs, all by Noah Kahan. Future work may expand the python script to take in user input, such as an artist or album, and provide songs that can be guessed.
This would include revamping the website to allow a toggle of possible artists/tracks.

The project may also be updated to add cookies to track user scores, and may consider switching to a daily model, where the song only changes once a day.

## Credits

Full credits for the lyrics and background image go to Noah Kahan and his team. I do not own any of the lyrical content or images.

Credits for supplying the lyrics go to [LRCLIB](https://lrclib.net/), and for allowing me to compile a list of songs and their durations, credits go to [LastFM](https://www.last.fm/).