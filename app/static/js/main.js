function showOverlay() {
    document.getElementById('overlay').classList.remove('visually-hidden');
}

function hideOverlay() {
    document.getElementById('overlay').classList.add('visually-hidden');
}

function minutesToHours(minutes) {
    var hours = Math.floor(minutes / 60);
    var remainingMinutes = minutes % 60;
    return hours + "H" + remainingMinutes;
}

function createResultBox(data) {
    var h1First = $("<h2 class='container mt-4 row p-2 result'>Voici le chemin le plus court</h2>")

    var h1Correspondance = $("<h2 class='container mt-4 row p-2 result'>Voici les correspondances</h2>")
    // Création de la section container
    var container = $("<section>").addClass("container mt-4");

    // Création de la première section pour le trajet final
    var finalSection = $("<section>").addClass("container mt-4");

    // Création de la div result avec la classe row et shadow-lg
    var resultDiv = $("<div>").addClass("row shadow-lg p-2 result");

    // Création de la première ligne
    var firstRow = $("<div>").addClass("row");
    var departure = $("<p>").addClass("").text(data.departure); // Départ du trajet final
    var arrow = $("<div>").addClass("arrow");
    var arrowIcon = $("<i>").addClass("fa-solid fa-arrow-down");
    var arrival = $("<p>").addClass("").text(data.arrival); // Arrivée du trajet final
    firstRow.append(departure, arrow.append(arrowIcon), arrival);

    // Création d'une ligne horizontale
    var hr = $("<hr>");

    // Création de la deuxième ligne pour la durée totale
    var secondRow = $("<div>").addClass("row");
    var clockDiv = $("<div>").addClass("col-md-1");
    var clockIcon = $("<i>").addClass("fa-solid fa-clock");
    clockDiv.append(clockIcon);
    var totalDuration = $("<p>").addClass("col-md-1").text(minutesToHours(data.total_duration)); // Conversion de la durée totale en heures
    secondRow.append(clockDiv, totalDuration);

    // Ajout des éléments à la div result
    resultDiv.append(firstRow, hr, secondRow);

    // Ajout de la div result à la section
    finalSection.append(resultDiv);

    // Ajout de la première section pour le trajet final au container
    container.append(h1First);

    container.append(finalSection);
    container.append(h1Correspondance);

    // Pour chaque étape de trajet
    data.steps.forEach(function (step) {
        // Création de la section pour chaque étape
        var section = $("<section>").addClass("container mt-4");

        // Création de la div result avec la classe row et shadow-lg
        var resultDiv = $("<div>").addClass("row shadow-lg p-2 result");

        // Création de la première ligne
        var firstRow = $("<div>").addClass("row");
        var departure = $("<p>").addClass("").text(step.from); // Utilisation de la donnée de départ de l'étape
        var arrow = $("<div>").addClass("arrow");
        var arrowIcon = $("<i>").addClass("fa-solid fa-arrow-down");
        var destination = $("<p>").addClass("").text(step.to); // Utilisation de la donnée d'arrivée de l'étape
        firstRow.append(departure, arrow.append(arrowIcon), destination);

        // Création d'une ligne horizontale
        var hr = $("<hr>");

        // Création de la deuxième ligne
        var secondRow = $("<div>").addClass("row");
        var clockDiv = $("<div>").addClass("col-md-1");
        var clockIcon = $("<i>").addClass("fa-solid fa-clock");
        clockDiv.append(clockIcon);
        var duration = $("<p>").addClass("col-md-1").text(minutesToHours(step.duration)); // Conversion de la durée de l'étape en heures
        secondRow.append(clockDiv, duration);

        // Ajout des éléments à la div result
        resultDiv.append(firstRow, hr, secondRow);

        // Ajout de la div result à la section
        section.append(resultDiv);

        // Ajout de la section au container
        container.append(section);
    });

    // Insérer la section container après la section avec la classe ".search-trajet"
    $(".search-trajet").after(container);

}

$(document).ready(function () {
    const actualBtn = document.getElementById('actual-btn');

    const fileChosen = document.getElementById('file-chosen');

    const btnMic = document.getElementById('pushed');

    const btnSearchSubmit = document.getElementById('btn-search');

    const textValue = document.getElementById('txt-value');

    // search with text

    btnSearchSubmit.addEventListener('click', function () {
        showOverlay();
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

                hideOverlay()
                if (!data.data.error) {
                    createResultBox(data.data)

                } else {
                    console.log("ERROR ICI ", data.data.error);
                    $(".message-alert").removeClass('d-none')
                    $("#message-alert-content").html(data.data.error)
                    hideOverlay()

                }
                // $("#txt-value").val(data.data["phrase"])

                // $("#reponse").html(data.data)
            })
            .catch(error => {
                console.log("ERROR ICI ");

                $(".message-alert").removeClass('d-none')
                $("#message-alert-content").html(error)
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
                // textValue.html(data.data)

                showOverlay();

                if (!data.data.error) {
                    hideOverlay()
                    if (data.data) {
                        $("#txt-value").val(data.data["phrase"])
                        createResultBox(data.data)


                    }
                    // console.log(data);
                    // stop pushed
                    $("#pushed").removeClass('pushed')


                } else {
                    $(".message-alert").removeClass('d-none')
                    // stop pushed
                    $("#pushed").removeClass('pushed')
                    $("#message-alert-content").html(data.data.error)
                    hideOverlay()

                }
                // console.log(data);



                // $("#reponse").html(data.data)
            })
            .catch(error => {
                console.log(error);
                $(".message-alert").removeClass('d-none')
                $("#message-alert-content").html(error)
                hideOverlay()
            });



    })

    // search with file
    actualBtn.addEventListener('change', function () {
        showOverlay();
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
                // console.log(data.data["phrase"]);
                console.log(data);
                if (!data.error) {
                    hideOverlay()
                    $("#txt-value").val(data.data["phrase"])

                    createResultBox(data.data)

                } else {
                    hideOverlay()

                    console.log(data.error);
                    $(".message-alert").removeClass('d-none')
                    $("#message-alert-content").html(data.error)
                }
                if (typeof(data.data) !== "undefined") {
                    
                }

                // console.log("YESS");
                // $("#reponse").html(data.data)
            })
            .catch(error => {
                // console.log(error);
                $(".message-alert").removeClass('d-none')
                $("#message-alert-content").html(error)

                hideOverlay()
            });
        // showOverlay()
        // hideOverlay()

    })

});