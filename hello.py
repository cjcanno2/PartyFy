from flask import Flask, render_template, url_for, copy_current_request_context, request, jsonify, Response, json
import requests
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
	#when form with value "Search for song" is requested
	if request.form['my-form'] == 'Search':
		text = request.form['songinput']
		#search spotify with input
		results = spotify.search(text, limit = 5, offset = 0, type = 'track')
		searchlist = results['tracks']['items']
		global trackResults
		#fill trackResults with spotify search results
		trackResults = searchlist
	else:
	#if it's not the top button, it's one of the song buttons
		slist = songList.getList()
		for song in slist:
			if int(request.form['my-form']) == song.getId():
				song.incrementScore()
				songList.sortList()
				break

	return render_template("index.html", songlist = songList.getList(), searchlist = searchlist)

#adds a song from a POST request
@app.route('/_add_song')
def add_song():
	#use song uri to find track's index in trackresults
	global currentid 
	currentid = currentid + 1
	songUri = request.args.get('songuri', "", type=str)
	print songUri
	for track in trackResults:
		if track['uri'] == songUri:
			currSong = track
			break

	#clear results
	searchlist = []
	trackresults = []

	#add song to queue, sort it accordingly
	songList.add(Song(currentid, currSong['name'], currSong['artists'][0]['name'], currSong['uri']))
	songList.sortList()

	#return the JSON of the track uri (JS does nothing with it at the moment, just need to return something)
	return jsonify(songname=songUri)

#returns all songs in songList in a json list, this function is polled by the javascript to update gui
@app.route('/_get_songlist')
def get_songlist():
	#return JSON string of all the songs in the list
	jsonlist = songList.toJSON()
	return Response(json.dumps(jsonlist),  mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', threaded=True)


