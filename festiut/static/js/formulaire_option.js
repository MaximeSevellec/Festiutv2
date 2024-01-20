function deselectionnerOption() {
    var selectElement = document.getElementById("selectionner-groupe");
    selectElement.selectedIndex = 0;
}

document.getElementById("formulaire-artiste").addEventListener("submit", function(event) {
    event.preventDefault();
});