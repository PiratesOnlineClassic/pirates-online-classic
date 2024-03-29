@echo off
title Pirates Online Classic - Client

rem Default config values
set TRIAL_ENDED=NO
set DEVELOPMENT_SERVER=158.69.1.129:6667
set TEST_SERVER=142.44.142.240
set PRODUCTION_SERVER=142.44.142.241
set GAME_SHOW_ADDS=YES

set GAME_INGAME_UPGRADE=https://www.piratesclassic.com/
set GAME_INGAME_MOREINFO=https:/www.piratesclassic.com/about
set GAME_INGAME_NAMING=https://www.piratesclassic.com/help/nameapprovals
set GAME_INGAME_MANAGE_ACCT=https://www.piratesclassic.com/account

rem Constants
SET LOCALHOST_SERVER=127.0.0.1
SET SETTINGS_FILE=../config/environ/default.env

rem Start launch operation and questioning
goto :READCONFIG

:READCONFIG
    set CONFIG_FILE=%SETTINGS_FILE%
    if exist %CONFIG_FILE% (
        for /F "tokens=*" %%A in (%CONFIG_FILE%) do call SET %%A
        goto :SETUPENVIRONMENT
    ) else (
        echo Failed to locate environment file: %CONFIG_FILE%

        pause
        goto :EOF
    )

:SETUPENVIRONMENT

    rem User variables
    set USERPROFILE=%USERPROFILE%

    rem Set Trial State
    if "%TRIAL_ENDED%" == "YES" (
        set GAME_SHOW_FIRSTADD=1
    )

    title Pirates Online Classic - Client (Trial Ended: %TRIAL_ENDED%)
    goto :CHOOSESERVER

:CHOOSESERVER
    rem Server address input selection
    echo Choose your server (Default: Localhost)
    echo    #1 - Localhost
    echo    #2 - Development
    echo    #3 - Public Test Server
    echo    #4 - Production Server
    echo    #5 - Custom

    set INPUT=1
    set /P INPUT=Selection: 

    set POC_GAMESERVER=%LOCALHOST_SERVER%
    if %INPUT%==1 (
        set POC_GAMESERVER=%LOCALHOST_SERVER%
    ) else if %INPUT%==2 (
        set POC_GAMESERVER=%DEVELOPMENT_SERVER%
    ) else if %INPUT%==3 (
        set POC_GAMESERVER=%TEST_SERVER%
    ) else if %INPUT%==4 (
        set POC_GAMESERVER=%PRODUCTION_SERVER%
    ) else if %INPUT%==5 (
        set /P POC_GAMESERVER=Client Agent IP: 
    ) else (
        echo Invalid Option: %INPUT%; Defaulting to Localhost
        set POC_GAMESERVER=%LOCALHOST_SERVER%
    )
    title Pirates Online Classic - Client (Server: %POC_GAMESERVER%)  (Trial Ended: %TRIAL_ENDED%)

    goto :ENVIRONMENTTYPE

:ENVIRONMENTTYPE

    rem Find default environment
    SET GAME_ENVIRONMENT=LIVE
    if %POC_GAMESERVER%==%LOCALHOST_SERVER% (
        set GAME_ENVIRONMENT=DEV
        set IS_TEST_SERVER=1
    ) else if %POC_GAMESERVER%==%DEVELOPMENT_SERVER% (
        set GAME_ENVIRONMENT=DEV
        set IS_TEST_SERVER=1
    ) else if %POC_GAMESERVER%==%TEST_SERVER% (
        set GAME_ENVIRONMENT=TEST
        set IS_TEST_SERVER=1
    ) else if %POC_GAMESERVER%==%PRODUCTION_SERVER% (
        set GAME_ENVIRONMENT=LIVE
        set IS_TEST_SERVER=0
    )

    goto :SETENVIRONEMNT

:SETENVIRONEMNT
    title Pirates Online Classic - Client (Server: %POC_GAMESERVER%) (Environment: %GAME_ENVIRONMENT%) (Trial Ended: %TRIAL_ENDED%)
    goto :PLAYTOKEN

:PLAYTOKEN
    rem PlayToken input
    set POC_TOKEN=dev
    if %POC_GAMESERVER%==%LOCALHOST_SERVER% (
        echo Set Username [Default: %POC_TOKEN%]
        set /P POC_TOKEN=Username:
    ) else if %POC_GAMESERVER%==%DEVELOPMENT_SERVER% (
        echo Set Username [Default: %POC_TOKEN%]
        set /P POC_TOKEN=Username:
    ) else (
        echo Set Account Token [Default: %POC_TOKEN%]
        set /P POC_TOKEN=Token:
    )    

    goto :FINDPYTHON

:FINDPYTHON
    rem Choose correct python command to execute the game
    ppythona -h >nul 2>&1 && (
        set PYTHON_CMD=ppythona
    ) || (
        set PYTHON_CMD=ppython
    )

    rem Verify Panda3D install
    %PYTHON_CMD% -h >nul 2>&1 && (
        rem Launch client
        goto :LAUNCH
    ) || (
        echo Failed to locate Panda3D python
        pause
        goto :EOF
    )

:LAUNCH
    echo =============================================
    echo Starting Pirates Online Classic...
    echo Token: %POC_TOKEN%
    echo Gameserver: %POC_GAMESERVER%
    echo Environment: %GAME_ENVIRONMENT%
    echo Trial Ended: %TRIAL_ENDED%
    echo PPython: %PYTHON_CMD%
    echo =============================================

    cd ../
    goto :RUN

:RUN
    rem Start the game using the PYTHON_CMD variable
    %PYTHON_CMD% -m pirates.piratesbase.PiratesStart
    pause

    rem Reload Client
    for /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set mydate=%%c-%%a-%%b)
    for /f "tokens=1-2 delims=/:" %%a in ('time /t') do (set mytime=%%a%%b)
    set RELOAD_TIME=%mydate%_%mytime%

    echo =============================================
    echo Reloading client. Time: %RELOAD_TIME%
    echo =============================================

    goto :RUN
