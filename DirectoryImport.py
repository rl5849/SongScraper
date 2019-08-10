import SongScraper
import config
import os


def RunDirectoryImport(directory, playlist):
    songScraper = SongScraper.SongScraper()
    songScraper.initialize()
    songScraper.ChangeLoggingDir(config.logging_path_itunes)
    songScraper.ChangePlaylist(playlist)


    mySongs = {}
    #for file in os.listdir(directory):
        #mySongs[songScraper.CleanSongString(splitline[0])] = songScraper.CleanSongString(splitline[1])


    songScraper.songs = mySongs
    songScraper.GetSpecificPlaylist()
    songScraper.AddSongsToPlayList()



