# classe modélisant une tâche (todo)
class ToDo:

    # constructeur
    def __init__(self,title,description,date_heure,etat):
        self.title = title              # titre
        self.description = description  # corps de la tâche
        self.date_heure = date_heure    # date de création
        self.etat = etat                # tâche complétée ou non

    # GETTERS 
    def get_title(self):
        return self.title
    
    def get_description(self):
        return self.description
    
    def get_date_heure(self):
        return self.date_heure

    def get_etat(self):
        return self.etat