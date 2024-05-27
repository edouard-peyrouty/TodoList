from controller import *

# filtre en cours
FILTRE = "processing"

# initialisation de l'application web
app = ToDo_controller.init()

# page principale du site (affichage des todos)
@app.route("/")
def display_todos():
    return ToDo_controller.display_todos(FILTRE)

# changement du filtre d'affichage
@app.route("/change/<filtre>")
def change_filter(filtre):
    global FILTRE
    FILTRE = filtre
    return display_todos()

# route de création d'un todo (mène vers la page d'acceuil) 
@app.route("/create", methods=['GET','POST'])
def create_todo():
    return ToDo_controller.create_todo(FILTRE)

# route d'édition d'un todo 
@app.route("/edit/<titre>/<description>", methods=["GET","POST"])
def edit(titre,description):
    return ToDo_controller.edit(titre,description,FILTRE)

# route de complétion d'un todo (on coche ou décoche la case)
@app.route('/cocher/<titre>', methods=['POST'])
def cocher(titre):
    return ToDo_controller.cocher(titre,FILTRE)

# route de suppression d'un todo (mène vers la page d'acceuil)
@app.route("/supprimer/<titre>")
def supprimer(titre):
    return ToDo_controller.delete_todo(titre,FILTRE)

# route de restauration d'un todo supprimé (mène vers la page d'acceuil)
@app.route("/restore/<titre>")
def restore(titre):
    return ToDo_controller.restore(titre)

# route de vidage de la corbeille (mène vers la page d'acceuil)
@app.route("/vider_corbeille")
def vider_corbeille():
    return ToDo_controller.vider_corbeille(FILTRE)

# porte d'entrée du programme
if __name__ == '__main__':
    app.run(debug=True)