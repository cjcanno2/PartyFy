import os
import hello
from song import Song, SongList


import unittest
import tempfile

class HelloTestCase(unittest.TestCase):

	def setUp(self):
		hello.app.config['TESTING'] = True
		self.app = hello.app.test_client()


	def tearDown(self):
		print "finishing..."
        #os.close(self.db_fd)
        #os.unlink(hello.app.config['DATABASE'])

	def test_create_song(self):
		print "testing if songs are created correctly"
		song = Song("TestSong", 1)
		assert 'TestSong' in song.getTitle()
		assert 1 == song.getId()

	def test_song_score(self):
		print "testing if song score is modified correctly"
		song = Song("TestSong", 1)
		assert 'TestSong' in song.getTitle()
		assert 1 == song.getScore()
		song.incrementScore()
		assert 2 == song.getScore()
		song.decrementScore()
		assert 1 == song.getScore()

	def test_create_songlist(self):
		print "testing if songlist is created correctly and can add/retrieve songs"
		songList = SongList()
		song = Song("TestSong", 1)
		songList.add(song)
		songtest = songList.getSongAt(0)
		assert 'TestSong' in songtest.getTitle()
		assert 1 == songtest.getId()

	def test_sort_songlist(self):
		print "testing if songlist sorts songs properly"
		songList = SongList()
		song1 = Song("TestSong1", 1)
		song2 = Song("TestSong2", 2)
		song2.incrementScore() 			#song2 should end up in index 0 after sort
		songList.add(song1)
		songList.add(song2)
		songList.sortList()
		songtest = songList.getSongAt(0)
		assert 'TestSong2' in songtest.getTitle()
		assert 2 == songtest.getId()



if __name__ == '__main__':
	unittest.main()



















