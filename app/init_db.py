"""
Script pour initialiser la base de données et vérifier la connexion
"""
import sys
import os

# Ajouter le répertoire parent au chemin Python
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from app.database import init_db
    from app.core.config import settings

    print("Configuration chargée avec succès.")
    print(f"URL de la base de données: {settings.DATABASE_URL}")

    try:
        print("Tentative d'initialisation de la base de données...")
        init_db()
        print("Base de données initialisée avec succès!")
        print("La table 'predictions' a été créée si elle n'existait pas déjà.")
    except Exception as error:  # pylint: disable=broad-exception-caught
        print(f"Erreur lors de l'initialisation de la base de données: {str(error)}")
        print("\nAssurez-vous que:")
        print("1. PostgreSQL est installé et en cours d'exécution")
        print("2. La base de données 'mobilitysoft_db' existe")
        print("3. Les identifiants dans le fichier .env sont corrects")

except ImportError as e:
    print(f"Erreur d'importation: {str(e)}")
    print("Vérifiez que toutes les dépendances sont correctement installées.")

print("\nAppuyez sur Entrée pour quitter...")
input()
