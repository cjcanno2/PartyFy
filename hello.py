from flask import Flask
from flask import request
from flask import render_template
from song import Song, SongList
import Queue

app = Flask(__name__)

songList = SongList()

#temporary solution to create unique IDs
currentid = 0

#initial template rendering
@app.route('/')
def my_form():
    return render_template("index.html", songlist = songList.getList())


#Takes input from template and adds it to the list
@app.route('/', methods=['POST'])
def my_form_post():

	if request.form['my-form'] == 'Add Song':
		text = request.form['songinput']
		global currentid 
		currentid = currentid + 1
		songList.add(Song(text, currentid))
		songList.sortList()
	else:
		slist = songList.getList()
		for song in slist:
			print "id is  ", song.getId()
			print "form s ", request.form['my-form']
			if int(request.form['my-form']) == song.getId():
				print "incrementing score!"
				song.incrementScore()
				songList.sortList()
				break

	return render_template("index.html", songlist = songList.getList())


if __name__ == '__main__':
    app.run(debug=True)











