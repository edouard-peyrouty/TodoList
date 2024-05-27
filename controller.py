from flask import Flask, render_template, request
from modele.repository import ToDoReposiroty 
from modele.bin import BinRepository  
from datetime import datetime

# classe controleur
class ToDo_controller:

    # initialise l'application web
    @staticmethod
    def init():
        # Crée la table 'todos' dans la base de données si elle n'existe pas déjà
        ToDoReposiroty.create_table()
        # Crée la table 'Bin' dans la base de données si elle n'existe pas déjà
        BinRepository.create_table()
        # on renvoie une instance de Flask
        return Flask(__name__)

    # récupère les todos et ouvre la page d'acceuil
    @staticmethod
    def display_todos(filtre,error=False):
        """
        affiche les todos selon le filtre (str) selectionné:
        - "all" : tous
        - "processing" : en cours
        - "completed" : complétés
        - "deleted" : supprimés (dans la corbeille)
        """
        # appelle la fonction modèle adaptée au filtre sélectioné
        if filtre == "all":
            todos = ToDoReposiroty.get_all_todos()
        elif filtre == "deleted":
            todos = BinRepository.get_all_todos()
        else:
            todos = ToDoReposiroty.get_todos(filtre)
        return render_template("display_todos.html",todos=todos,filtre=filtre,error=error)
    
    # gère la création d'un nouveau todo
    @staticmethod
    def create_todo(filtre):
        # ouvre la page de création d'un todo
        if request.method == 'GET':
            return render_template('create_todo.html')
        # crée le todo
        elif request.method == 'POST':
            # récupère les infos constituants le todo (titre, corps, date)
            title = request.form['title']
            description = request.form['description']
            date_heure = datetime.today()
            # stocke le todo dans la base de données
            if ToDoReposiroty.create_todo(title,description,date_heure):
                # renvoie sur la page de création si le titre n'est pas valide
                return render_template('create_todo.html',error=True,description=description)
            # affiche la page d'acceuil
            return ToDo_controller.display_todos(filtre)

    # gère l'édition d'un todo
    @staticmethod
    def edit(titre,description,filtre):
        # Ouvre la page d'édition du todo
        if request.method == "GET":
            return render_template("edit.html",titre=titre,description=description)
        # modifie le todo
        else:
            # supprime le todo de la DB
            ToDoReposiroty.delete_todo(titre)
            # créer un nouveau todo avec les nouvelles informations
            return ToDo_controller.create_todo(filtre)
        
    # gère la case à cocher (todo finie ou non)
    @staticmethod
    def cocher(titre,filtre):
        # on détermine si elle a été cochée ou non
        if "checkbox" in request.form:
            etat_case = request.form["checkbox"]
        else:
            etat_case = False   
        # on met à jour l'état du todo dans la BD
        ToDoReposiroty.change_etat(titre,etat_case)
        # affiche la page d'acceuil
        return ToDo_controller.display_todos(filtre)
    
    # suppression d'un todo
    @staticmethod
    def delete_todo(titre,filtre):
        # récupère les informations du todo
        todo = ToDoReposiroty.get_todo(titre)
        # supprime de la BD
        ToDoReposiroty.delete_todo(titre)
        # ajoute le todo dans la corbeille
        BinRepository.add_todo(todo)
        # affiche page d'acceuil
        return ToDo_controller.display_todos(filtre)
    
    # restauration d'un todo de la corbeille
    @staticmethod
    def restore(titre):
        # on récupère les informations du todo
        todo = BinRepository.get_todo(titre)
        # on le crée dans la BD des todos sinon on annule l'appoération et affiche un message d'erreur
        if ToDoReposiroty.create_todo(todo.get_title(),todo.get_description(),datetime.today()):
            return ToDo_controller.display_todos("deleted",error=True)
        # on le supprime de la corbeille
        BinRepository.delete_todo(titre)
        # on redirige vers la page d'acceuil
        return ToDo_controller.display_todos("deleted")
    
    # vide la corbeille
    @staticmethod
    def vider_corbeille(filtre):
        BinRepository.delete_all_todos()
        return ToDo_controller.display_todos(filtre)