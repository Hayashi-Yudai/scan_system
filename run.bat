@echo off
cd /d %~dp0

set PORT=8000

start chrome.exe http://localhost:%PORT%/core/
start python.exe manage.py runserver %PORT%