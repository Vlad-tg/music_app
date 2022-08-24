var audio_track = document.getElementById('audio_track');
var currentTime = document.getElementById("currentTime");
var durationTime = document.getElementById("durationTime");
var listAudio = document.querySelectorAll(".button-player-block-track");


function createTrackItem(index, name, duration) {
    var listAudio = document.querySelector(".button-player-block-track")
    listAudio.setAttribute("data-index", "" + index);
    listAudio.setAttribute("id", "track-id-" + index);
    document.querySelector(".player-song").appendChild(listAudio);

    var list_img = document.createElement('img');
    list_img.setAttribute("src", "/static/core/img/img_playlist_player/play_player.svg");
    list_img.setAttribute("height", "30");
    list_img.setAttribute("width", "30");

    list_img.setAttribute("class", "play-img-main");
    list_img.setAttribute("id", "play-img-" + index);
    document.querySelector(".player-song").appendChild(list_img);
}


var listAudio_t = document.querySelectorAll(".button-player-block-track")
listAudio_t.forEach(function (audioSingle, index) {
    createTrackItem(index)
})

var indexAudio = 0;

function progressValue() {
    audio_track.max = player.duration
    audio_track.value = player.currentTime

    currentTime.textContent = getMinutes(player.currentTime)
    durationTime.textContent = getMinutes(player.duration)
}

timer = setInterval(progressValue, 500);

function changeProgressBar() {
    player.currentTime = audio_track.value;
}

audio_track.addEventListener("click", changeProgressBar);

function loadNewTrack(index) {
    var player = document.querySelector('#source-id')
    player.src = listAudio[index].getAttribute('data-audio');
    document.querySelector("#hidden-play-id").style.display = 'none';
    document.querySelector("#play").style.display = 'block';
    document.querySelector('.div-base-playlist-player-track-title').innerHTML = listAudio[index].getAttribute('data-name')
    document.querySelector('.div-base-playlist-player-track-author').innerHTML = listAudio[index].getAttribute('data-author')
    document.querySelector('.img-base-playlist-player-track-image').src = listAudio[index].getAttribute('data-image')
    document.querySelector(".div-base-playlist-a-two").style.display = "block";
    document.querySelector(".div-base-playlist-a-two-right").style.display = "block";
    this.player = document.getElementById("audio");
    this.player.load()
    this.toggleAudio()
    this.updateStylePlaylist(this.indexAudio, index)
    this.indexAudio = index;

}

var playListItems = document.querySelectorAll(".button-player-block-track");


for (let i = 0; i < playListItems.length; i++) {
    playListItems[i].addEventListener("click", getClickedElement.bind(this));
}


function getClickedElement(event, oldIndex) {
    for (let i = 0; i < playListItems.length; i++) {
        if (playListItems[i] === event.target) {
            var clickedIndex = event.target.getAttribute("data-index")
            var data_actives = event.target.getAttribute("data-active")
            if (clickedIndex === this.indexAudio || data_actives === "active") {
                this.toggleAudio()
            } else {
                listAudio[indexAudio].removeAttribute("data-active")
                loadNewTrack(clickedIndex);
            }
        }
    }
}

document.querySelector('#source-audio').src = listAudio[indexAudio].getAttribute('data-audio')
document.querySelector('.div-base-playlist-player-track-title').innerHTML = listAudio[indexAudio].getAttribute('data-name')
document.querySelector('.div-base-playlist-player-track-author').innerHTML = listAudio[indexAudio].getAttribute('data-author')
document.querySelector('.img-base-playlist-player-track-image').src = listAudio[indexAudio].getAttribute('data-image')

var player = document.getElementById("audio")
player.load()

function clickAD() {
    const play = document.querySelector("#play")
    const hidden_play_id = document.querySelector("#hidden-play-id")

    const data_active_play = document.querySelector("#play").getAttribute('data-active-play')
    if (data_active_play === 'pass') {
        document.getElementById('track-id-0').click();
        play.setAttribute('data-active-play', 'none')
        play.style.display = 'block';
        hidden_play_id.style.display = 'none';
    }
}

function toggleAudio() {

    if (this.player.paused) {
        document.querySelector('#track-id-' + this.indexAudio).classList.add("active-track");
        document.querySelector(".img-base-playlist-player-pause").style.display = "block"
        document.querySelector(".img-base-playlist-player-play").style.display = "none"
        document.querySelector(".div-base-playlist-player-track-image").classList.add("active-image");
        this.playToPause(this.indexAudio)
        this.player.play();
    } else {
        document.querySelector(".img-base-playlist-player-pause").style.display = "none"
        document.querySelector(".img-base-playlist-player-play").style.display = "block"
        document.querySelector(".div-base-playlist-player-track-image").classList.remove("active-image");

        this.pauseToPlay(this.indexAudio)
        this.player.pause();
    }
}

function nextAudioAfterAudio() {
    if (this.player.ended) {
        var oldIndex = this.indexAudio
        this.indexAudio++;
        updateStylePlaylist(oldIndex, this.indexAudio)
        this.loadNewTrack(this.indexAudio);

    }
}

function nextAudio() {
    if (this.indexAudio < listAudio.length - 1) {
        var oldIndex = this.indexAudio
        listAudio[indexAudio].removeAttribute("data-active")
        this.indexAudio++;
        listAudio[indexAudio].setAttribute("data-active", 'active');
        updateStylePlaylist(oldIndex, this.indexAudio)
        this.loadNewTrack(this.indexAudio);

    }

}

function previousAudio() {
    if (this.indexAudio > 0) {
        var oldIndex = this.indexAudio
        listAudio[indexAudio].removeAttribute("data-active")
        this.indexAudio--;
        listAudio[indexAudio].setAttribute("data-active", 'active');
        updateStylePlaylist(oldIndex, this.indexAudio)
        this.loadNewTrack(this.indexAudio);
    }
}

var width = 0;

function getMinutes(t) {
    var min = parseInt(parseInt(t) / 60);
    var sec = parseInt(t % 60);
    if (sec < 10) {
        sec = "0" + sec
    }
    if (min < 10) {
        min = "0" + min
    }
    return min + ":" + sec
}


function forward() {
    this.player.currentTime = this.player.currentTime + 5
    var progress = (this.player.currentTime / this.player.duration) * 100;

}

function rewind() {
    this.player.currentTime = this.player.currentTime - 5
    var progress = (this.player.currentTime / this.player.duration) * 100;

}

function updateStylePlaylist(oldIndex, newIndex) {
    document.querySelector('#track-id-' + oldIndex).classList.remove("active-track");
    this.pauseToPlay(oldIndex);
    document.querySelector('#track-id-' + newIndex).classList.add("active-track");
    this.playToPause(newIndex)
}

function playToPause(index) {
    var ele = document.querySelector('#play-img-' + index)
    ele.removeAttribute("src");
    ele.setAttribute("src", "/static/core/img/img_playlist_player/pause_player.svg");
}

function pauseToPlay(index) {
    var ele = document.querySelector('#play-img-' + index)
    ele.removeAttribute("src");
    ele.setAttribute("src", "/static/core/img/img_playlist_player/play_player.svg");
}
