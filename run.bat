@echo off
cd /d %~dp0

set PORT=8000
set CONDA_ENV=thz

call activate %CONDA_ENV%
call python.exe webgui.py
call deactivate
