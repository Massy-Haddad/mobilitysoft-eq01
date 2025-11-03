@echo off
REM Script pour exécuter les tests de MobilitySoft
REM Usage: tests.bat [all|unit|integration]

if "%1"=="" goto usage

if /i "%1"=="all" goto all
if /i "%1"=="unit" goto unit
if /i "%1"=="integration" goto integration
goto usage

:all
echo ====================================
echo Execution de TOUS les tests
echo ====================================
.venv\Scripts\python.exe -m pytest tests/ -v
goto end

:unit
echo ====================================
echo Execution des TESTS UNITAIRES
echo ====================================
.venv\Scripts\python.exe -m pytest tests/ -v -m unit
goto end

:integration
echo ====================================
echo Execution des TESTS D'INTEGRATION
echo ====================================
.venv\Scripts\python.exe -m pytest tests/ -v -m integration
goto end

:usage
echo.
echo Usage: tests.bat [all^|unit^|integration]
echo.
echo   all           - Execute tous les tests
echo   unit          - Execute uniquement les tests unitaires
echo   integration   - Execute uniquement les tests d'integration
echo.
goto end

:end
