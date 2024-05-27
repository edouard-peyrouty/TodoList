from sqlite3 import *
from modele.todo import ToDo

class BinRepository:

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
        BinRepository.requete_sql('''CREATE TABLE IF NOT EXISTS Bin (
                            title TEXT NOT NULL PRIMARY KEY,
                            description TEXT NOT NULL,
                            date_heure DATE NOT NULL,
                            etat BOOLEAN NOT NULL)''') 

    # ajoute un todo dans la corbeille
    @staticmethod
    def add_todo(todo):
        # si le todo qu'on veut ajouter à le même titre qu'un déjà existant on l'écrase
        if BinRepository.get_todo(todo.get_title()):
            BinRepository.requete_sql(f"""DELETE FROM Bin WHERE title='{todo.get_title()}';""")
        # on ajoute le todo dans la BD
        BinRepository.requete_sql(f"""INSERT INTO Bin VALUES('{todo.get_title()}',
                                  '{todo.get_description()}',
                                  '{todo.get_date_heure()}',
                                  '{todo.get_etat()}')""")
        
    # renvoie la liste des todos de la BD sous la forme d'un tableau d'objets ToDo
    @staticmethod
    def get_all_todos():
        todos = BinRepository.requete_sql('''SELECT * FROM Bin ORDER BY date_heure DESC''',True)
        return [ToDo(todo[0],todo[1],todo[2],(todo[3] == "TRUE")) for todo in todos]
    
    # récupère les information d'un todo à partir de son titre
    @staticmethod
    def get_todo(titre):
        todo = BinRepository.requete_sql(f"""SELECT * FROM Bin WHERE title='{titre}';""",True)
        # ne renvoie les informations que si le todo existe
        if todo:
            return ToDo(todo[0][0],todo[0][1],todo[0][2],(todo[0][3] == "TRUE"))
        
    # supprime un todo de la BD
    @staticmethod
    def delete_todo(titre):
        BinRepository.requete_sql(f"""DELETE FROM Bin WHERE title='{titre}';""")

    # supprime tous les todos de la corbeille
    @staticmethod
    def delete_all_todos():
        BinRepository.requete_sql("""DELETE FROM Bin""")

    