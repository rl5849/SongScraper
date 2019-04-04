###
#Author: rl5849
#Github: github.com/rl5849
##

import requests
import secrets
from Logging import Logging
import re
import spotipy as spotipy
import spotipy.util as util
from urllib.parse import unquote_plus

auth_url = 'https://accounts.spotify.com/api/token'
songs_list = "recentEvents" #Name of the json element that contains the list of songs
title_string = 'title' #Json elements for song and artist
artist_string = 'artist'
scope = 'playlist-modify-public'
redirect_uri = "http://localhost:8000"

class SongScraper:
    sp = None
    token = ""
    playlist_id = ""
    songs = {}
    songs_already_in_playlist = {}
    songs_added = 0
    logger = None

    def GetPlaylistFromWeb(self):
        songs = {}
        page = requests.get(secrets.Station_URL)
        if(page.status_code == 200):
            print("Got the playlist")
        else:
            print("Couldn't get playlist")
            return

        #parse json
        json = page.json()

        #Get the item that has all the
        songs_json = json[songs_list]

        for song_json in songs_json:
            songs[self.CleanSongString(song_json[title_string])] = unquote_plus(song_json[artist_string])

        self.songs = songs

        return


    def CleanSongString(self, string):
        #Url decode
        string = unquote_plus(string)

        #Remove non alphanumeric
        re.sub(r'([^\s\w]|_)+', '', string)

        string = re.sub("&", "", string)
        string = re.sub("\.", "", string)


        #Remove Hashtagged prefixes to the songs
        unhashtagged = re.match("^#.*? - (.*)", string)
        string = unhashtagged.groups()[0] if unhashtagged else string

        #remove 'Ft' and beyond
        unfeatured = re.match("^(.*?).Ft", string)
        string = unfeatured.groups()[0] if unfeatured else string

        unfeatured = re.match("^(.*?).ft", string)
        string = unfeatured.groups()[0] if unfeatured else string

        unfeatured = re.match("^(.*?).feat", string)
        string = unfeatured.groups()[0] if unfeatured else string

        return string.strip()


    def GetSpecificPlaylist(self):
        playlists = self.sp.user_playlists(secrets.User_Name)

        playlist_id = 0
        for playlist_item in playlists['items']:
            if(playlist_item["name"] == secrets.Spotify_Playlist_Name):
                playlist_id = playlist_item["id"]
                break

        return playlist_id

    def AddSongsToPlayList(self):
        track_ids = []

        for song, artist in self.songs.items():
            result = self.sp.search(song+" "+artist, limit=1, offset=0, type='track')
            song_result = result['tracks']['items']

            if len(song_result) > 0:
                song_id = song_result[0]['id']
                #Dont add duplicates
                if song_id not in self.songs_already_in_playlist:
                    track_ids.append(song_id)
                    self.songs_already_in_playlist.append(song_id)
                    self.songs_added += 1
                    self.logger.logInfo("Adding song to playlist: {} by {}".format(song, artist))

                if len(track_ids) >= 50:
                    track_ids.clear()
            else:
                self.logger.logError("Search failed for songs: {} by {}".format(song, artist))

        #Periodically sends 50, send remainders
        if len(track_ids) > 0:
            self.SendSongsToSpotify(track_ids)
        return

    def SendSongsToSpotify(self, track_ids):
        if len(track_ids) > 0:
            self.sp.user_playlist_add_tracks(user=secrets.User_Name, playlist_id=self.playlist_id, tracks=track_ids,
                                         position=0)
            self.logger.logInfo("Pushing new batch of {} more songs".format(self.songs_added))
        else:
            self.logger.logError("Didn't get any songs to send")


    def GetPlaylistContents(self):
        song_ids = []
        foundAllSongs = False
        currentOffset = 0

        if not self.playlist_id:
            return

        #Spotify only delivers 100 songs at a time, I want them all
        while not foundAllSongs:
            currentPlaylistContents = self.sp.user_playlist_tracks(secrets.User_Name, playlist_id=self.playlist_id, fields='items(track(id))',market=None, offset=currentOffset)

            foundAllSongs = (len(currentPlaylistContents['items']) < 100)

            for song in currentPlaylistContents['items']:
                song_ids.append(song['track']['id'])
            currentOffset += 100

        return song_ids


    def initialize(self):
        self.logger = Logging()

        #Get list of songs from web
        if len(self.songs) <= 0:
            self.GetPlaylistFromWeb()
            if len(self.songs) > 0:
                print("Successfully retrieved playlist")
            else:
                print("Failed to get playlist from web!")
                return False

        #Get auth token
        if not self.token or self.sp is None:
            token = util.prompt_for_user_token(secrets.User_Name, scope, client_id=secrets.Client_ID,
                                               client_secret=secrets.Client_Secret, redirect_uri=redirect_uri)
            self.sp = spotipy.Spotify(auth=token)

            if not self.token or self.sp is None:
                print("Successfully got auth token")
            else:
                print("Failed to get auth token!")
                return False

        #Get playlist ID
        if not self.playlist_id:
            self.playlist_id = self.GetSpecificPlaylist()
            if self.playlist_id:
                print("Successfully got playlist ID")
            else:
                print("Failed to get playlist ID!")
                return False

        self.songs_already_in_playlist = self.GetPlaylistContents()
        if self.songs_already_in_playlist:
            print("Successfully got playlist from spotify")
        else:
            print("Failed to get playlist from spotify!")
            return False

        return True



    def main(self):
        if not self.initialize():
            self.logger.logInfo("Unknown Error!")
            return
        self.logger.logInfo("Starting new run")

        self.AddSongsToPlayList()
        self.logger.logInfo("Done! Added {} new songs!".format(self.songs_added))
        return



if __name__ == '__main__':
    songScraper = SongScraper()
    songScraper.main()