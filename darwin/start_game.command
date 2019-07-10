#!/bin/sh
cd ..

export DYLD_LIBRARY_PATH=`pwd`/Libraries.bundle
export DYLD_FRAMEWORK_PATH="Frameworks"

# Get the user input:
read -p "Username: " pocUsername
read -p "Gameserver (DEFAULT:  127.0.0.1): " POC_GAMESERVER
POC_GAMESERVER=${POC_GAMESERVER:-"127.0.0.1"}

# Export the environment variables:
export pocUsername=$pocUsername
export pocPassword="password"
export POC_TOKEN=$pocUsername
export POC_GAMESERVER=$POC_GAMESERVER

export GAME_INGAME_UPGRADE="https://www.piratesclassic.com/"
export GAME_INGAME_MOREINFO="https:/www.piratesclassic.com/about"
export GAME_INGAME_NAMING="https://www.piratesclassic.com/help/nameapprovals"
export GAME_INGAME_MANAGE_ACCT="https://www.piratesclassic.com/account"
export GAME_ENVIRONMENT="DEV"
export GAME_SHOW_FIRSTADD=0
export GAME_SHOW_ADDS="YES"

echo "==============================="
echo "Starting Pirates Online Classic..."
echo "Username: $pocUsername"
echo "Gameserver: $POC_GAMESERVER"
echo "==============================="

python -m pirates.piratesbase.PiratesStart
