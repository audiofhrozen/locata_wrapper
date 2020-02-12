@echo off
SET DISPLAY=:0
SET "THIS_DIR=%cd%"
CD ..\..\


SET "ROOT_DIR=%cd%"

CALL tools\venv\condabin\activate.bat
CD %THIS_DIR%
echo %ROOT_DIR%