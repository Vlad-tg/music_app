const audio_track_id = document.getElementById('audio_track');
const current_time = document.getElementById("currentTime");
const duration_time = document.getElementById("durationTime");
const player = document.getElementById("audio_id");

function progressValueTrack() {
    audio_track_id.max = player.duration;
    audio_track_id.value = player.currentTime;

    current_time.textContent = getMinutesTrack(player.currentTime);
    duration_time.textContent = getMinutesTrack(player.duration);

}

timer = setInterval(progressValueTrack, 500);


function changeProgressBarTrack() {
    player.currentTime = audio_track_id.value;
}

audio_track_id.addEventListener("click", changeProgressBarTrack);


function playToPauses() {

    const track = document.querySelector('.button-player-block-track')
    const player = document.getElementById('audio_id')

    const img_pause = document.querySelector('.img_pause')
    const img_play = document.querySelector('.img_play')

    const track_data_active = track.getAttribute('data-active')

    if (track_data_active === "") {
        img_play.style.display = 'none';
        img_pause.style.display = 'block';
        player.load();
        player.play();
        track.setAttribute("data-active", "active");
        document.querySelector('.div-base-song-block-audio-player').style.display = 'block';
        document.querySelector('.img-base-song-play').style.display = 'none';
        document.querySelector('.img-base-song-pause').style.display = 'block';
    } else if (track_data_active === "active") {
        player.pause();
        track.setAttribute("data-active", "pause");
         img_play.style.display = 'block';
        img_pause.style.display = 'none';
        document.querySelector('.img-base-song-play').style.display = 'block';
        document.querySelector('.img-base-song-pause').style.display = 'none';


    } else {
        player.play();
        track.setAttribute("data-active", "active");
         img_play.style.display = 'none';
        img_pause.style.display = 'block';
        document.querySelector('.img-base-song-play').style.display = 'none';
        document.querySelector('.img-base-song-pause').style.display = 'block';
    }
}


function getMinutesTrack(t) {
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


function nextAudioAfterAudio() {
    const player = document.getElementById('audio_id')
    const track = document.querySelector('.button-player-block-track')


    if (player.ended) {
        player.pause();
        track.setAttribute("data-active", "pause");

        document.querySelector('.img_play').style.display = 'block';
        document.querySelector('.img_pause').style.display = 'none';
        document.querySelector('.img-base-song-play').style.display = 'block';
        document.querySelector('.img-base-song-pause').style.display = 'none';
    }
}


function forwards() {
    player.currentTime = player.currentTime + 5
    var progress = (player.currentTime / player.duration) * 100;

}

function rewinds() {
    player.currentTime = player.currentTime - 5
    var progress = (player.currentTime / player.duration) * 100;

}

