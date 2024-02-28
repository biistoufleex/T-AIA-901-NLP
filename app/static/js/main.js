function showOverlay() {
    document.getElementById('overlay').classList.remove('visually-hidden');
}

function hideOverlay() {
    document.getElementById('overlay').classList.add('visually-hidden');
}

$(document).ready(function () {
    const actualBtn = document.getElementById('actual-btn');

    const fileChosen = document.getElementById('file-chosen');

    const btnMic = document.getElementById('pushed');

    const btnSearchSubmit = document.getElementById('btn-search');

    const textValue = document.getElementById('txt-value');

    // search with text

    btnSearchSubmit.addEventListener('click', function () {

        fetch('/searchText', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                trajet: textValue.value
            }),
        })
            .then(response => response.json())
            .then(data => {
                console.log(data);
                if (!data.error) {
                    showOverlay();
                } else {
                    $(".message-alert").removeClass('d-none')
                    $("#message-alert-content").html(data.error)
                    hideOverlay()

                }
                $("#reponse").html(data.data)
            })
            .catch(error => {
                $(".message-alert").removeClass('d-none')
                $("#message-alert-content").html(data.error)
                hideOverlay()
            });

    })


    // search with voice

    btnMic.addEventListener('click', function () {
        this.classList.add("pushed");

        console.log(this);
        fetch('/voiceRecognize', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({}),
        })
            .then(response => response.json())
            .then(data => {
                if (!data.error) {
                    showOverlay();
                } else {
                    $(".message-alert").removeClass('d-none')
                    // stop pushed
                    $("#pushed").removeClass('pushed')
                    $("#message-alert-content").html(data.error)
                    hideOverlay()

                }
                $("#reponse").html(data.data)
            })
            .catch(error => {
                $(".message-alert").removeClass('d-none')
                hideOverlay()
            });



    })

    // search with file
    actualBtn.addEventListener('change', function () {
        var file = this.files[0]
        console.log('file:', this.files[0]);
        var formData = new FormData();
        formData.append('file', this.files[0]);
        // set name file choose
        fileChosen.textContent = this.files[0].name
        fetch('/voiceRecognizeFile', {
            method: 'POST',
            body: formData,
        })
            .then(response => response.json())
            .then(data => {
                console.log(data);
                if (!data.error) {
                    showOverlay();
                } else {
                    console.log(data.error);
                    $(".message-alert").removeClass('d-none')
                    $("#message-alert-content").html(data.error)
                }
                $("#reponse").html(data.data)
            })
            .catch(error => {
                $(".message-alert").removeClass('d-none')
                $("#message-alert-content").html(data.error)

                hideOverlay()
            });
        // showOverlay()
        // hideOverlay()

    })

});