@echo off
title Pirates Online Classic - Client

rem Server address input selection
echo Choose your server (Default: Localhost)
echo #1 - Localhost
echo #2 - Development
echo #3 - Custom

set INPUT=-1
set /P INPUT=Selection: 

set POC_GAMESERVER=127.0.0.1
if %INPUT%==1 (
    set POC_GAMESERVER=127.0.0.1
) else if %INPUT%==2 (
    set POC_GAMESERVER=47.133.210.240
) else if %INPUT%==3 (
    set /P POC_GAMESERVER=Game Server IP: 
) else (
    set POC_GAMESERVER=127.0.0.1
)
title Pirates Online Classic - Client (%POC_GAMESERVER%)


rem PlayToken input
set /P POC_TOKEN=Token (Default: dev): || ^
set POC_TOKEN=dev

rem Choose correct python command to execute the game
ppythona -h >nul 2>&1 && (
    set PYTHON_CMD=ppythona
) || (
    set PYTHON_CMD=ppython
)

echo ====================================
echo Starting Pirates Online Classic...
echo Token: %POC_TOKEN%
echo Gameserver: %POC_GAMESERVER%
echo PPython: %PYTHON_CMD%
echo ====================================

cd ../

rem Start the game using the PYTHON_CMD variable
:main
%PYTHON_CMD% -m pirates.piratesbase.PiratesStart
pause
goto :main
