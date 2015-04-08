#Created by Evan Richter

class Song: 

    def __init__(self, title):
    	self.title = title
    	self.score = 1

    def getTitle(self):
    	return self.title
    def setTitle(self, newtitle):
    	self.title = newtitle

    def getScore(self):
        return self.score
    def setScore(self, newscore):
        self.score = newscore

class SongList:

    def __init__(self):
        self.list = []

    def getList(self):
        return self.list

    def getListAt(self, index):
        return self.list[index]

    def add(self, song):
        self.list.append(song)

    def sortList(self):
        self.list.sort(self.compare_songs)

    def compare_songs(self, song1, song2):
        return song1.getScore() - song2.getScore()