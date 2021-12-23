@echo off
cd /d %~dp0

set PORT=8000
set CONDA_ENV=thz


REM start chrome.exe http://localhost:%PORT%

call activate %CONDA_ENV%
REM call python.exe manage.py runserver %PORT%
call python.exe gui.py
call deactivate
