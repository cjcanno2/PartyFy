from flask import Flask
from flask import request
from flask import render_template
from song import Song, SongList
import Queue

app = Flask(__name__)

songList = SongList()

@app.route('/')
def my_form():
    return render_template("index.html", songqueue = songList.getList())

#Takes input from form and adds it to the queue
@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    songList.add(Song(text))
    songList.sortList()
    return render_template("index.html", songlist= songList.getList())

if __name__ == '__main__':
    app.run(debug=True)