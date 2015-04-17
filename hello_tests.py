import os
import hello
from song import Song, SongList
import spotipy

spotify = spotipy.Spotify()


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
		song = Song(1, "TestSong", "TestArtist", 0)
		assert 'TestSong' in song.getTitle()
		assert 1 == song.getId()

	def test_song_score(self):
		print "testing if song score is modified correctly"
		song = Song(1, "TestSong", "TestArtist", 0)
		assert 'TestSong' in song.getTitle()
		assert 1 == song.getScore()
		song.incrementScore()
		assert 2 == song.getScore()
		song.decrementScore()
		assert 1 == song.getScore()

	def test_create_songlist(self):
		print "testing if songlist is created correctly and can add/retrieve songs"
		songList = SongList()
		song = Song(1, "TestSong", "TestArtist", 0)
		songList.add(song)
		songtest = songList.getSongAt(0)
		assert 'TestSong' in songtest.getTitle()
		assert 1 == songtest.getId()

	def test_sort_songlist(self):
		print "testing if songlist sorts songs properly"
		songList = SongList()
		song1 = Song(1, "TestSong1", "TestArtist", 0)
		song2 = Song(2, "TestSong2", "TestArtist", 0)
		song2.incrementScore() 			#song2 should end up in index 0 after sort
		songList.add(song1)
		songList.add(song2)
		songList.sortList()
		songtest = songList.getSongAt(0)
		assert 'TestSong2' in songtest.getTitle()
		assert 2 == songtest.getId()

	def test_get_search_results(self):
		print "testing if search result data is correctly extracted"
		text = "wonderwall"
		results = spotify.search(text, limit = 10, type = 'track')
		assert 'Wonderwall' in results['tracks']['items'][0]['name']

	def test_add_search_results(self):
		print "testing if chosen search result is added correctly"
		text = "wonderwall"
		results = spotify.search(text, limit = 10, type = 'track')
		title = results['tracks']['items'][0]['name']
		artist = results['tracks']['items'][0]['artists'][0]['name']
		uri = results['tracks']['items'][0]['uri']
		song1 = Song(1, title, artist, uri)
		assert 'Wonderwall' in song1.getTitle()
		assert 'Oasis' in song1.getArtist()






if __name__ == '__main__':
	unittest.main()



















