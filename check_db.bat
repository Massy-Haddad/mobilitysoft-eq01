@echo off
echo Activation de l'environnement virtuel...
call .venv\Scripts\activate.bat

echo Vérification de la base de données...
python app\init_db.py

pause
