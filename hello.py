from flask import Flask
from flask import request
from flask import render_template
from song import Song, SongList
import Queue
import spotipy

spotify = spotipy.Spotify()

app = Flask(__name__)

songList = SongList()

trackResults = []

#temporary solution to create unique IDs
currentid = 0

@app.route('/')
def my_form():
    return render_template("index.html", songlist = songList.getList())

#Takes input from template and adds it to the list
@app.route('/', methods=['POST'])
def my_form_post():

	searchlist = []
	if request.form['my-form'] == 'Add Song':
		text = request.form['songinput']
		results = spotify.search(text, limit = 10, offset = 0, type = 'track')
		searchlist = results['tracks']['items']
		global trackResults
		trackResults = searchlist
	else:
		slist = songList.getList()
		for song in slist:
			#print "id is  ", song.getId()
			#print "form s ", request.form['my-form']
			if int(request.form['my-form']) == song.getId():
				#print "incrementing score!"
				song.incrementScore()
				songList.sortList()
				break

	return render_template("index.html", songlist = songList.getList(), searchlist = searchlist)


@app.route('/enqueue', methods = ['POST'])
def enqueue():
	global currentid 
	currentid = currentid + 1
	songName = request.form['add-song']
	index = songName.find(": ")
	index = songName[:index]
	currSong = trackResults[int(index)-1]
	songList.add(Song(currentid, currSong['name'], currSong['artists'][0]['name'], currSong['uri']))
	songList.sortList()
	return render_template("index.html", songlist = songList.getList())

if __name__ == '__main__':
    app.run(debug=True)











