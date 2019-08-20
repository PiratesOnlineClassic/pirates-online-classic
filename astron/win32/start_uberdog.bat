@echo off
title Pirates Online Classic - UberDOG
cd ../../

rem Choose correct python command to execute the game
ppythona -h >nul 2>&1 && (
    set PYTHON_CMD=ppythona
) || (
    set PYTHON_CMD=ppython
)

echo ============================================
echo Starting Pirates Online Classic UberDOG...
echo PPython: %PYTHON_CMD%
echo ============================================

rem Start UberDOG server
:main
%PYTHON_CMD% -m pirates.uberdog.ServiceStart 
goto main