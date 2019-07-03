@echo off
setlocal enableextensions enabledelayedexpansion
call "path.bat"
call "cmd.bat"

set VERBOSE=INFO
set PROCESS=1

set CONFIG_FILE=conf\default_locata_dev.yaml

rem Argument parser routine
:loop
if not "%1"=="" (
    set "test=%1"
    if /i "!test:~0,2!"=="--" (
        set var=!test:~2!
        if defined !var! (
            set "!var!=%2"
            shift
        )
    )
    shift 
    goto loop
)
rem end routine

cd ..

python locata_wrapper/bin/eval_loc.py -l %VERBOSE% ^
                                      with %CONFIG_FILE% ^
                                      processes=%PROCESS%


:eof
cd win
echo %~nx0 Done.
endlocal