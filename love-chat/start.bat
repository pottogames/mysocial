@echo off
cd /d "%~dp0"
:loop
node run.js
echo השרת נפל, מפעיל מחדש בעוד 5 שניות...
timeout /t 5 >nul
goto loop
