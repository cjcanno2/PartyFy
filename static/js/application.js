
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
        $.getJSON("_add_song", {
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

            //slice off starting and ending " characters
            songname = JSON.stringify(value.songname).substring(1).slice(0, -1);
            artistname = JSON.stringify(value.artistname).substring(1).slice(0, -1);
            score = JSON.stringify(value.score).substring(1).slice(0, -1);

            //build HTML string of button for songs in list
            song_string += "<form action=\".\" method=\"POST\"> \n" ;
            song_string += "<button class=\"songbutton\" type=\"submit\" name=\"my-form\" value=" + JSON.stringify(value.idnum) + ">";
            song_string += songname + " - " + artistname + " - " + score + "</button> \n";
            song_string += "</form>";
        });
         
        $('.songlist').html(song_string);/*.animate({
                opacity: 1 // Animate opacity to 1 with a duration of 1 sec
            }, 1000);
        */
    });
}
setInterval('get_songlist()', 2000);

function play_song() {
    
        
    var def = $.Deferred();

    (function loop() {

        console.log("inside while loop");

        $.getJSON("_play_songs", 
            function (data) {

                console.log(data["url"]);
                console.log(data["length"]);


                if(String(data["url"]) === "none"){
                    def.resolve();
                }
                
                else{
                    songWindow = window.open(data["url"], '_blank');
                    get_songlist();

                    window.setTimeout(function(){
                        songWindow.close();
                        def.notify();
                        loop();
                    }, data["length"] + 10000);
                }

            });
    })();


    return def.promise();        
    
}


$(function() {

    $('.playbutton').bind('click', function() {

        play_song().progress(function() {

        }).done(function() {

        });

    });

});







