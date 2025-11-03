@echo off
echo ============================================
echo Configuration de Pre-commit pour MobilitySoft
echo ============================================
echo.

echo Activation de l'environnement virtuel...
call .venv\Scripts\activate.bat

echo.
echo Installation des dependances de developpement...
pip install -r requirements.txt

echo.
echo Installation des hooks pre-commit...
pre-commit install

echo.
echo Execution des hooks sur tous les fichiers...
pre-commit run --all-files

echo.
echo ============================================
echo Configuration terminee!
echo ============================================
echo.
echo Les hooks pre-commit sont maintenant actifs.
echo Ils s'executeront automatiquement avant chaque commit.
echo.
echo Pour tester manuellement: pre-commit run --all-files
echo Pour executer les tests: pytest
echo.
pause
