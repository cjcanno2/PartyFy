from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
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

#temporary solution to create unique IDs
currentid = 0


redirect_uri = "http://localhost:5000/login"

sp_oauth = spotipy.oauth2.SpotifyOAuth(clientId, clientSecret, redirect_uri, 
	scope=scope, cache_path=".cache-" + username)

@app.route('/')
def my_form():

	token = sp_oauth.get_cached_token()

	#if not token:
	return redirect(sp_oauth.get_authorize_url())
	
	return render_template("index.html", songlist = songList.getList())

	



@app.route('/login')
def login_success():
	url = request.url
	code = sp_oauth.parse_response_code(url)
	token = sp_oauth.get_access_token(code)
	spotify = spotipy.Spotify(token['access_token'])
	spotify.user_playlist_create(spotify.me()["id"], "456", public = False)
	return render_template("login.html", url = url)

#Takes input from template and adds it to the list
@app.route('/', methods=['POST'])
def my_form_post():

	searchlist = []
	if request.form['my-form'] == 'Add Song':
		text = request.form['songinput']
		results = spotify.search(text, limit = 5, offset = 0, type = 'track')
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











