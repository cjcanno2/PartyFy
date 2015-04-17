from flask import Flask, render_template, url_for, copy_current_request_context, request, jsonify, Response, json, redirect
import requests
from song import Song, SongList
import Queue
import spotipy
import spotipy.util as util

spotify = spotipy.Spotify()

app = Flask(__name__)

songList = SongList()

trackResults = []

username = "1263203807"

clientId = "41ca80c15e3943a9b191dc9d4d279608"

clientSecret = "15705cd588f54f1fa407e238fb63cbdf"

scope = "playlist-modify-private"

playlistName = "partyfy"

playlist = ""

#temporary solution to create unique IDs
currentid = 0


redirect_uri = "http://localhost:5000/login"

sp_oauth = spotipy.oauth2.SpotifyOAuth(clientId, clientSecret, redirect_uri, 
	scope=scope, cache_path=".cache-" + username)

@app.route('/')
def my_form():

	token = sp_oauth.get_cached_token()

	if not token:
		return redirect(sp_oauth.get_authorize_url())
	
	return render_template("index.html", songlist = songList.getList())

	



@app.route('/login')
def login_success():
	url = request.url
	code = sp_oauth.parse_response_code(url)
	token = sp_oauth.get_access_token(code)

	global spotify
	spotify = spotipy.Spotify(token['access_token'])

	#newPlaylist = spotify.user_playlist_create(spotify.me()["id"], playlistName, public = False)
	#global playlist
	#playlist = newPlaylist
	
	return render_template("index.html", songlist = songList.getList(), searchlist = [])


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
	songList.add(Song(currentid, currSong['name'], currSong['artists'][0]['name'], currSong["duration_ms"], currSong['uri']))
	songList.sortList()

	#return the JSON of the track uri (JS does nothing with it at the moment, just need to return something)
	return jsonify(songname=songUri)

#returns all songs in songList in a json list, this function is polled by the javascript to update gui
@app.route('/_get_songlist')
def get_songlist():
	#return JSON string of all the songs in the list
	jsonlist = songList.toJSON()
	return Response(json.dumps(jsonlist),  mimetype='application/json')



@app.route('/_play_songs')
def play_songs():

	if(songList.getLength() == 0):
		return jsonify(url = "none")

	song = songList.getAndRemoveSongAt(0)
	#spotify.user_playlist_add_tracks(spotify.me()["id"], playlist["id"], [song.getUri()])
	url = song.getUri()
	index = url.find("track:") + 6
	url = url[index:]
	url = "https://play.spotify.com/track/" + url
	return jsonify(url = url, length = song.getLength())


if __name__ == '__main__':
    app.run(debug=True, threaded=True)


