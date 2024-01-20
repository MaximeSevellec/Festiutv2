function envoyerFormulaireGroupe() {
    if ($('#formulaire-groupe')[0].checkValidity()) {
        var formData = new FormData($('#formulaire-groupe')[0]);
        
        $.ajax({
            type: 'POST',
            url: '/ajouter_nouveau_groupe',
            data: formData,
            contentType: false,
            processData: false,
            success: function(response) {
                if (response.success) {
                    window.location.reload(true);
                } else {
                    $('#message-groupe').text(response.message);
                }
            },
            error: function(error) {
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
            success: function(response) {
                if (response.success) {
                    window.location.reload(true);
                } else {
                    $('#message-artiste').text(response.message);
                }
            },
            error: function(error) {
                console.log(error);
            }
        });
    }
}