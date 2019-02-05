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

echo "==============================="
echo "Starting Pirates Online Classic..."
echo "Username: $pocUsername"
echo "Gameserver: $POC_GAMESERVER"
echo "==============================="

python -m pirates.piratesbase.PiratesStart
