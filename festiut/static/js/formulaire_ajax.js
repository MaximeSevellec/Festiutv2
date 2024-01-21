function envoyerFormulaireGroupe() {
    if ($('#formulaire-groupe')[0].checkValidity()) {
        var formData = new FormData($('#formulaire-groupe')[0]);

        $.ajax({
            type: 'POST',
            url: '/ajouter_nouveau_groupe',
            data: formData,
            contentType: false,
            processData: false,
            success: function (response) {
                if (response.success) {
                    window.location.reload(true);
                } else {
                    $('#message-groupe').text(response.message);
                }
            },
            error: function (error) {
                console.log(error);
            }
        });
    }
}

function envoyerFormulaireArtiste() {
    if ($('#formulaire-artiste')[0].checkValidity()) {
        var formData = new FormData($('#formulaire-artiste')[0]);

        $.ajax({
            type: 'POST',
            url: '/ajouter_nouveau_artiste',
            data: formData,
            contentType: false,
            processData: false,
            success: function (response) {
                if (response.success) {
                    window.location.reload(true);
                } else {
                    $('#message-artiste').text(response.message);
                }
            },
            error: function (error) {
                console.log(error);
            }
        });
    }
}

function envoyerFormulaireFestival() {
    if ($('#formulaire-festival')[0].checkValidity()) {
        var formData = new FormData($('#formulaire-festival')[0]);

        $.ajax({
            type: 'POST',
            url: '/ajouter_nouveau_festival',
            data: formData,
            contentType: false,
            processData: false,
            success: function (response) {
                if (response.success) {
                    window.location.reload(true);
                } else {
                    $('#message-festival').text(response.message);
                }
            },
            error: function (error) {
                console.log(error);
            }
        });
    }
}

function envoyerFormulaireEvent() {
    if ($('#formulaire-event')[0].checkValidity()) {
        var formData = new FormData($('#formulaire-event')[0]);

        $.ajax({
            type: 'POST',
            url: '/ajouter_nouveau_event',
            data: formData,
            contentType: false,
            processData: false,
            success: function (response) {
                if (response.success) {
                    window.location.reload(true);
                } else {
                    $('#message-event').text(response.message);
                }
            },
            error: function (error) {
                console.log(error);
            }
        });
    }
}

function envoyerFormulaireAssignerGroupe(button) {
    if ($('#formulaire-assigner-groupe')[0].checkValidity()) {
        idEvent = $(button).attr('data-idEvent');
        var formData = new FormData($('#formulaire-assigner-groupe')[0]);

        $.ajax({
            type: 'POST',
            url: '/assigner_nouveau_groupe_event/' + idEvent,
            data: formData,
            contentType: false,
            processData: false,
            success: function (response) {
                if (response.success) {
                    window.location.href = "/assigner_groupe_event_sans_groupe/";
                } else {
                    $('#message-assigner-groupe').text(response.message);
                }
            },
            error: function (error) {
                console.log(error);
            }
        });
    }
}