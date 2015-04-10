#Created by Evan Richter

class Song: 

    def __init__(self, title, idnum):
    	self.title = title
    	self.score = 1
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








