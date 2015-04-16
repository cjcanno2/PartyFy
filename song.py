#Created by Evan Richter

class Song: 

    def __init__(self, idnum, title, artist, uri):
    	self.title = title
    	self.score = 1
        self.artist = artist
        self.uri = uri
        self.id = idnum

    def getTitle(self):
    	return self.title
    def setTitle(self, newtitle):
    	self.title = newtitle

    def getId(self):
        return self.id
    def setId(self, newid):
        self.id = newid

    def getScore(self):
        return self.score
    def setScore(self, newscore):
        self.score = newscore
    def incrementScore(self):
        self.score = self.score + 1
    def decrementScore(self):
        self.score = self.score - 1

    def toJSON(self):
        song_json  = "{ \"idnum\":\"" + str(self.id) 
        song_json += "\", \"songname\":\"" + self.title 
        song_json += "\", \"artistname\":\"" + self.artist 
        song_json += "\", \"uri\":\"" + self.uri 
        song_json += "\", \"score\":\"" + str(self.score) + "\"}"

        return song_json




class SongList:

    def __init__(self):
        self.list = []

    def getList(self):
        return self.list

    def getSongAt(self, index):
        return self.list[index]

    def add(self, song):
        self.list.append(song)

    #sort list with highest score at the top
    def sortList(self):
        self.list.sort(self.compare_songs)

    def compare_songs(self, song1, song2):
        return song2.getScore() - song1.getScore()

    #return JSON list of all the entries
    def toJSON(self):
        list_json = "["
        if (self.getList()):
            for song in self.list:
                list_json += song.toJSON() + ","
            list_json = list_json[:-1]
        list_json += "]"
        return list_json





