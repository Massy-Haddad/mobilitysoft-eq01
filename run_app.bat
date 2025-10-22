@echo off
echo Activation de l'environnement virtuel...
call .venv\Scripts\activate.bat

echo Installation des dépendances...
pip install -r requirements.txt

echo Connexion à PostgreSQL sur localhost:5432...
echo Si l'application échoue, vérifiez que PostgreSQL est en cours d'exécution.
echo.

echo Lancement de l'application...
uvicorn app.main:app --reload

pause