@echo off
echo === Pokretanje Flask aplikacije lokalno ===

:: Postavljanje Flask okruženja
set FLASK_APP=app.py
set FLASK_ENV=development

:: Pokretanje servera
python -m flask run --host=0.0.0.0 --port=5059

pause
