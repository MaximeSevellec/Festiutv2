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
