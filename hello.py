from flask import Flask
from flask import request
from flask import render_template
from song import Song, SongList
import Queue
import spotipy

spotify = spotipy.Spotify()

app = Flask(__name__)

songList = SongList()

results = []

@app.route('/')
def my_form():
    return render_template("index.html", songlist = songList.getList())

#Takes input from form and adds it to the queue
@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    results = spotify.search(text, limit = 10, offset = 0, type = 'track')
    #songList.add(Song(text))
    #songList.sortList()
    return render_template("index.html", songlist= songList.getList(), searchlist = results['tracks']['items'])

@app.route('/enqueue', methods = ['POST'])
def enqueue():
	songName = request.form['add-song']
	index = songName.find(": ")
	songName = songName[:index]
	songList.add(Song(songName))
	songList.sortList()
	return render_template("index.html", songlist = songList.getList())

if __name__ == '__main__':
    app.run(debug=True)