// On s'assure que ce bout de code s'execte après le chargement de la page
document.addEventListener("DOMContentLoaded", function() {
    // on récupère la liste des checkbox de la page qui sont associé à des tâches complétées (class=True)
    var checkboxes = document.querySelectorAll('input[type="checkbox"].True');
    // on précoche ces checkbox
    checkboxes.forEach(function(checkbox) {
        checkbox.checked = true;
    });
});

alert(document.getElementById("test").style.color);


// quand on coche un todo
function cocher(form_id){
    // on récupère le formulaire associé à la case qui à été (dé)cochée
    var formulaire = document.getElementById(form_id);
    // on soumet le formulaire
    formulaire.submit();
}

