function deselectionnerOption() {
    var selectElement = document.getElementById("selectionner-groupe");
    selectElement.selectedIndex = 0;
}

var formulaireArtiste = document.getElementById("formulaire-artiste");
if (formulaireArtiste !== null) {
    formulaireArtiste.addEventListener("submit", function(event) {
        event.preventDefault();
    });
}

var formulaireGroupe = document.getElementById("formulaire-groupe");
if (formulaireGroupe !== null) {
    formulaireGroupe.addEventListener("submit", function(event) {
        event.preventDefault();
    });
}

var formulaireFestival = document.getElementById("formulaire-festival");
if (formulaireFestival !== null) {
    formulaireFestival.addEventListener("submit", function(event) {
        event.preventDefault();
    });
}

var formulaireEvent = document.getElementById("formulaire-event");
if (formulaireEvent !== null) {
    formulaireEvent.addEventListener("submit", function(event) {
        event.preventDefault();
    });
}
