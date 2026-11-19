
@echo off

title Sandoval TI - Sistema

cd /d "%~dp0"

echo =====================================
echo       SANDOVAL TI - SISTEMA
echo =====================================
echo.

echo Ativando ambiente Python...

call .venv\Scripts\activate.bat

if errorlevel 1 (
    echo.
    echo ERRO: Nao foi possivel ativar o ambiente virtual.
    pause
    exit /b
)

echo.
echo Iniciando sistema...

start "" http://127.0.0.1:8000

python manage.py runserver

pause
