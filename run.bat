@echo off
cd /d %~dp0

set PORT=8000
set CONDA_ENV=thz

start chrome.exe http://localhost:%PORT%/core/

call conda activate %CONDA_ENV%
call python.exe manage.py runserver %PORT%
call conda deactivate