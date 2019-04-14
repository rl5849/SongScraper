import main


def ItunesToSpotify(file):
    songScraper = main.SongScraper()
    songScraper.initialize()

    with open(file, 'r', encoding='utf-8') as fp:
        line  = fp.readline()
        count = 1
        mySongs = {}
        while line:
            splitline = line.strip().split("\t")
            mySongs[songScraper.CleanSongString(splitline[0])] = songScraper.CleanSongString(splitline[1])
            line = fp.readline()
            count += 1

        songScraper.songs = mySongs
        songScraper.GetSpecificPlaylist()
        songScraper.AddSongsToPlayList()

