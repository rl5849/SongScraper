import SongScraper
import config
import os
import eyed3



# We need to look at a specfic directory, match those songs with songs in local files dir,
# use those IDs to say to add the songs to a specific playlist

def RunDirectoryImport(directory, playlist):
    songScraper = SongScraper.SongScraper()
    songScraper.playlist = playlist
    songScraper.initialize()
    songScraper.ChangeLoggingDir(config.logging_path_itunes)
    songScraper.ChangePlaylist(playlist)

    for file in os.listdir(directory):
        with os.scandir(directory) as dir_entries:
            for entry in dir_entries:
                audiofile = eyed3.load(entry.path)
                if(audiofile is not None):
                    songScraper.songs[audiofile.tag.title] = audiofile.tag.artist
        break


    mySongs = {}
    #for file in os.listdir(directory):
        #mySongs[songScraper.CleanSongString(splitline[0])] = songScraper.CleanSongString(splitline[1])


    songScraper.songs = mySongs
    songScraper.GetSpecificPlaylist()
    songScraper.AddSongsToPlayList()



