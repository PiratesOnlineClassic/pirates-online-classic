@echo off
title Pirates Online Classic - Client

rem Config Settings
set TRIALENDED=NO

rem User variables
set USERPROFILE=%USERPROFILE%

rem Set Advertising values
set GAME_SHOW_ADDS=YES
if "%TRIALENDED%" == "YES" (
    set GAME_SHOW_FIRSTADD=1
)

rem Set Website Links
set GAME_INGAME_UPGRADE=https://www.piratesclassic.com/
set GAME_INGAME_MOREINFO=https:/www.piratesclassic.com/about
set GAME_INGAME_NAMING=https://www.piratesclassic.com/help/nameapprovals
set GAME_INGAME_MANAGE_ACCT=https://www.piratesclassic.com/account

rem Start operation
goto :CHOOSESERVER

:CHOOSESERVER
    rem Server address input selection
    echo Choose your server (Default: Localhost)
    echo    #1 - Localhost
    echo    #2 - Development
    echo    #3 - Custom

    set INPUT=-1
    set /P INPUT=Selection: 

    set POC_GAMESERVER=127.0.0.1
    if %INPUT%==1 (
        set POC_GAMESERVER=127.0.0.1
    ) else if %INPUT%==2 (
        set POC_GAMESERVER=142.44.142.239
    ) else if %INPUT%==3 (
        set /P POC_GAMESERVER=Game Server IP: 
    ) else (
        set POC_GAMESERVER=127.0.0.1
    )
    title Pirates Online Classic - Client (%POC_GAMESERVER%)

    goto :ENVIRONMENTTYPE

:ENVIRONMENTTYPE
    rem Environment input
    set INPUT=DEV
    set /P INPUT=Environment (LIVE, QA, TEST, DEV) (Default: %INPUT%): 

    for %%G in (LIVE QA TEST DEV) do (
        if "%INPUT%"=="%%G" (
            set GAME_ENVIRONMENT=%INPUT%
            goto :SETENVIRONEMNT
        )
    )
    goto :INVALIDENVIRONMENT

:INVALIDENVIRONMENT
    echo %GAME_ENVIRONMENT% is not a valid environment; Default to DEV
    set GAME_ENVIRONMENT=DEV
    goto :SETENVIRONEMNT

:SETENVIRONEMNT
    echo Client environment set to: %GAME_ENVIRONMENT%
    title Pirates Online Classic - Client (%POC_GAMESERVER%) (%GAME_ENVIRONMENT%)
    goto :PLAYTOKEN

:PLAYTOKEN
    rem PlayToken input
    set POC_TOKEN=dev
    echo Set Account Token (Default: %POC_TOKEN%)
    set /P POC_TOKEN=Token:
    
    goto :FINDPYTHON

:FINDPYTHON
    rem Choose correct python command to execute the game
    ppythona -h >nul 2>&1 && (
        set PYTHON_CMD=ppythona
    ) || (
        set PYTHON_CMD=ppython
    )

    %PYTHON_CMD% -h >nul 2>&1 && (
        goto :LAUNCH
    ) || (
        echo Failed to locate Panda3D python
        pause
        goto :EOF
    )

:LAUNCH
    echo ====================================
    echo Starting Pirates Online Classic...
    echo Token: %POC_TOKEN%
    echo Gameserver: %POC_GAMESERVER%
    echo Environment: %GAME_ENVIRONMENT%
    echo Trial Ended: %TRIALENDED%
    echo PPython: %PYTHON_CMD%
    echo ====================================

    cd ../
    goto :RUN

:RUN
    rem Start the game using the PYTHON_CMD variable
    %PYTHON_CMD% -m pirates.piratesbase.PiratesStart

    pause
    echo Reloading client.
    goto :RUN
