# SongScraper

## Create Spotify playlists from radio station playlists or import an itunes playlist

#### Usage
```
  -h, --help            show this help message and exit
  --itunes_import FILE  Do you want to specify a file to import an iTunes
                        library from.
  --playlist PLAYLIST   Spotify playlist to import into.
  --web_import          Do you want to import songs from the web.
  --dir_import          Do you want to import songs from a local directory
    --directoy          directory to read

```


```--web_import```

Like a local radio stations playlist, but don't want to sit there and search songs and drag them to a playlist? Song scraper can quickly parse a JSON list of songs, find them on Spotify®, and add them to a playlist for you. Many stations already have endpoints that their own websites use to display and update their recently played songs (Finding them takes a bit of time to do in a browsers debugger)

#### Configuring for web import
* Register as a Spotify Dev and enter your Client_ID & Client_Secret in the config file.
* Use a web console debugger to step through your stations website to find the JSON endpoint it is getting the playlist from and add this to the config file.
* In the config file set the name of the playlist you want to dump the songs into.
* [optional] Fill in the log directories for the script.
* Run ```python3 SongScraper.py --web_import --playlist {playlist_name}```


```--itunes_import```
#### Importing from Itunes
* Open Itunes, go to ```File > Library > Export Playlist...```
* Save the file as a Text file
* Run ```python3 SongScraper.py --itunes_import {path/to/file} --playlist {playlist_name}```

After each run, check the log to see if any songs could not be found on Spotify
