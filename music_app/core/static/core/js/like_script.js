const list_index = 0;

const form_like = document.querySelectorAll("form[name=form_like]")
form_like.forEach(function (formLike, index) {

    const input_like = document.querySelectorAll(".input-audio-player-like")
     for (let i = 0; i < input_like.length; i++) {
        input_like[i].setAttribute('id', 'input-audio-player-like-id-' + i)
    }
     const label_like = document.querySelectorAll(".label-audio-player-like-active")
     for (let i = 0; i < label_like.length; i++) {
        label_like[i].setAttribute('for', 'input-audio-player-like-id-' + i)
    }
      const label_not_like = document.querySelectorAll(".label-audio-player-like-not-active")
     for (let i = 0; i < label_not_like.length; i++) {
        label_not_like[i].setAttribute('for', 'input-audio-player-like-id-' + i)
    }

})

















    // form_like.forEach(function (formLike, index) {

        // createLikeItem(index)

    // });

    // function loadNewTrack(index) {
    //     // const like = document.querySelector(".input-audio-player-like")
    //     let data = new FormData(this);
    //     const data_active = like_id_index[index].getAttribute('data-active')
    //     if (data_active === '') {
    //         like_id_index[index].setAttribute('data-active', 'active')
    //         fetch(`${this.action}`, {
    //             method: 'POST',
    //             body: data,
    //         })
    //             .then(response => console.log(response))
    //             .then(success => console.log(success))
    //             .catch(error => console.log(error))
    //     } else {
    //         like_id_index[index].setAttribute('data-active', '')
    //         fetch(`${this.action}`, {
    //             method: 'POST',
    //             body: data,
    //
    //         })
    //             .then(response => console.log(response))
    //             .then(success => console.log(success))
    //             .catch(error => console.log(error))
    //
    //     }
    // }
    // like_id_index[index].addEventListener("click", function (e) {





