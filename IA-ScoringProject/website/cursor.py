import sqlite3

# Se connecter à la base de données
conn = sqlite3.connect('/home/dorian/Python Linux/Projets Finaux/E1/instance/database.db')
cursor = conn.cursor()

# Supprimer les enregistrements avec les IDs 1, 2 et 3
#ids_to_delete = (1, 2, 3)
cursor.execute("DELETE FROM History WHERE id = 1")

# Confirmer les modifications et fermer la connexion
conn.commit()
conn.close()
