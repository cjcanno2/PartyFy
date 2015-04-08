from flask import Flask
from flask import request
from flask import render_template
from song import Song, SongList
import Queue

app = Flask(__name__)

songList = SongList()

@app.route('/')
def my_form():
    return render_template("index.html", songlist = songList.getList())


#Takes input from form and adds it to the list
@app.route('/', methods=['POST'])

def my_form_post():

	if request.form['my-form'] == 'add':
		text = request.form['songinput']
		songList.add(Song(text))
		songList.sortList()
	else:
		slist = songList.getList()
		for song in slist:
			if request.form['my-form'] == song.getTitle():
				song.incrementScore()
				songList.sortList()
				break

	return render_template("index.html", songlist = songList.getList())


if __name__ == '__main__':
    app.run(debug=True)











