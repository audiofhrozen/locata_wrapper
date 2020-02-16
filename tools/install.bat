@echo off
setlocal enableextensions enabledelayedexpansion

set URL=https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe
set "THIS_DIR=%cd%"
set PYTHON_VERSION=3.7


if "%~1" == "" goto :miniconda.sh
if /I %1 == clean goto :clean

:clean
@RD /S /Q %THIS_DIR%\venv
del miniconda3.exe
goto :EOF


:miniconda.sh
powershell Invoke-WebRequest -Uri '%URL%' -OutFile 'miniconda3.exe'


:venv
start /wait "" miniconda3.exe /InstallationType=JustMe /RegisterPython=0 /AddToPath=0 /S /D=%THIS_DIR%\venv
rem similar to activate in bash
call %THIS_DIR%\venv\condabin\activate.bat
start /wait "" cmd /c conda install -y setuptools -c anaconda
start /wait "" cmd /c conda install -y pip -c anaconda
start /wait "" cmd /c conda update -y conda
start /wait "" cmd /c conda install -y python=%PYTHON_VERSION%


:locata_wrapper.done
call %THIS_DIR%\venv\condabin\activate.bat
start /wait "" cmd /c conda install -y matplotlib
start /wait "" cmd /c  conda install -y numpy
start /wait "" cmd /c conda install -y h5py
pip install -e ..


:EOF
echo install.bat Done.
endlocal
