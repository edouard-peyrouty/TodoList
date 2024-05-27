from sqlite3 import *
from modele.todo import ToDo

# classe modèle (gestion des requête à la BD todos.db)
class ToDoReposiroty:

    # exécute une requête sql
    @staticmethod
    def requete_sql(requete,is_select=False):
        """
        requete (char) : requête sql
        is_select (bool) : true si la requête est un select false sinon
        """
        # connexion à la DB
        conn = connect('data/todos.db')
        # curseur pour exécuter des requêtes SQL
        cursor = conn.cursor()
        # exécution de la requête
        cursor.execute(requete)
        # si la requête est un select
        if is_select:
            # récupération des résultats de la requête
            rec = cursor.fetchall()
            # fermeture de la connexion
            conn.close()
            # renvoie des infos
            return rec
        else:
            # validation des changements
            conn.commit()    
            # fermeture de la connexion
            conn.close()

    # crée la BD
    @staticmethod
    def create_table():
        ToDoReposiroty.requete_sql('''CREATE TABLE IF NOT EXISTS Todos (
                            title TEXT NOT NULL PRIMARY KEY,
                            description TEXT NOT NULL,
                            date_heure DATE NOT NULL,
                            etat BOOLEAN NOT NULL)''')  
    
    # insère un todo dans la BD
    @staticmethod
    def create_todo(title,description,date_heure):
        # si le todo qu'on veut créer a le même titre qu'un déjà existant on renvoie True pour faire remonter l'erreur
        if ToDoReposiroty.get_todo(title):
            return True
        # si tout va bien on l'insère dans la BD
        else:
            ToDoReposiroty.requete_sql(f"""INSERT INTO todos VALUES("{title}","{description}","{date_heure}",'FALSE')""")

    # renvoie la liste des todos de la BD sous la forme d'un tableau d'objets ToDo
    @staticmethod
    def get_all_todos():
        todos = ToDoReposiroty.requete_sql('''SELECT * FROM todos ORDER BY date_heure DESC''',True)
        return [ToDo(todo[0],todo[1],todo[2],(todo[3] == "TRUE")) for todo in todos]
    
    # renvoie la liste des todos complétés ou bien non complétés de la BD sous la forme d'un tableau d'objets ToDo
    @staticmethod
    def get_todos(etat):
        etat = "TRUE" if etat == "completed" else "FALSE"
        todos = ToDoReposiroty.requete_sql(f'''SELECT * FROM todos WHERE etat='{etat}' ORDER BY date_heure DESC''',True)       
        return [ToDo(todo[0],todo[1],todo[2],(todo[3] == "TRUE")) for todo in todos]
    
    # change dans la BD l'état de complétion d'une Todo donnée (titre(str) : titre de la todo, etat(str) : "on" si la case est cochée)
    @staticmethod
    def change_etat(titre,etat):
        etat = "TRUE" if etat == "on" else "FALSE"
        return ToDoReposiroty.requete_sql(f"""UPDATE todos SET etat='{etat}' WHERE title='{titre}';""")

    # supprime un todo de la BD
    @staticmethod
    def delete_todo(titre):
        ToDoReposiroty.requete_sql(f"""DELETE FROM todos WHERE title='{titre}';""")

    # récupère les information d'un todo à partir de son titre
    @staticmethod
    def get_todo(titre):
        todo = ToDoReposiroty.requete_sql(f"""SELECT * FROM Todos WHERE title='{titre}';""",True)
        # ne renvoie les informations que si le todo existe
        if todo:
            return ToDo(todo[0][0],todo[0][1],todo[0][2],(todo[0][3] == "TRUE"))