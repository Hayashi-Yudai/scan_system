@echo off
set /P ANSWER="Start building measurement environment. Continue (Y/N)?"

if /i {%ANSWER%}=={Y} (goto :yes)
if /i {%ANSWER%}=={y} (goto :yes)
if /i {%ANSWER%}=={yes} (goto :yes)

EXIT

:yes

set CONDA_ENV=thz

call conda create -n %CONDA_ENV% python=3.9 -y
call conda activate %CONDA_ENV%
call pip install -r requirements.txt
call conda deactivate