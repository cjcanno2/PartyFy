
/*

$(function() { 
    $('.searchsongbutton').bind('click', function() {
            //animate opening the result list
            $('.resultlist').animate({
                height: 1000 // Animate height with a duration of 1/4 sec
            }, 250);   

        return false;
    }); 
});

*/

$(function() { 
    $('.searchresultbutton').bind('click', function() {
        //TODO: change IP to something general
        $.getJSON("http://10.0.0.8:5000/_add_song", {
            songuri: this.id
        }, function(data) {
            //clear search results in gui

            $('.resultlist').animate({
                height: 0 // Animate height to 0 with a duration of 1/4 sec
            }, 250);

            $('.resultlist').html("");
            //update songlist gui 
            get_songlist()      
        });

        return false;

    }); 
});

function get_songlist() {
    $.getJSON("_get_songlist", function (data) {
        songdata = $.parseJSON(data)
        song_string = '';
        $.each(songdata, function(key, value) { 
            //console.log (JSON.stringify(key) + ":" + JSON.stringify(value.songname));
            //song_string = song_string + '<p>' + JSON.stringify(value.songname) + '</p>';

            //build HTML string of button for songs in list
            song_string += "<form action=\".\" method=\"POST\"> \n" ;
            song_string += "<button class=\"songbutton\" type=\"submit\" name=\"my-form\" value=" + JSON.stringify(value.idnum) + ">";
            song_string += JSON.stringify(value.songname).replace("\"", "").replace("\"", "") + " - " + JSON.stringify(value.artistname).replace("\"", "").replace("\"", "")
            song_string += " - " + JSON.stringify(value.score).replace("\"", "").replace("\"", "") + "</button> \n";
            song_string += "</form>";
        });
         
        $('.songlist').html(song_string);/*.animate({
                opacity: 1 // Animate opacity to 1 with a duration of 1 sec
            }, 1000);
        */
    });
}
setInterval('get_songlist()', 2000);







