@echo off
set /P ANSWER="Start building measurement environment. Continue (Y/N)?"

if /i {%ANSWER%}=={Y} (goto :yes)
if /i {%ANSWER%}=={y} (goto :yes)
if /i {%ANSWER%}=={yes} (goto :yes)

exit

:yes
set CONDA_ENV=thz
set PYTHON_VERSION=3.9

call :CreateEnv
call :ActivateEnv
call :InstallLibraries
call :Deactivate

echo Success!
pause

exit

:CreateEnv
call conda create -n %CONDA_ENV% python=%PYTHON_VERSION% -y
if %errorlevel% neq 0 (
	echo Failed to create Python environment for measurement
	pause
	exit 
)

exit /b

:ActivateEnv
call conda activate %CONDA_ENV%
if %errorlevel% neq 0 (
	echo Failed to activate Python environment for measurement
	pause
	exit
)

exit /b

:InstallLibraries
call pip install -r requirements.txt
if %errorlevel% neq 0 (
	echo Failed to install libraries
	pause
	exit
)

exit /b

:Deactivate
call conda deactivate
if %errorlevel% neq 0 (
	echo Failed to deactivate Python environment for measurement
	pause
	exit
)

exit /b