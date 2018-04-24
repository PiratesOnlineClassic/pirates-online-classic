#!/bin/sh
cd ..

export DYLD_LIBRARY_PATH=`pwd`/Libraries.bundle
export DYLD_FRAMEWORK_PATH="Frameworks"

# Get the user input:
read -p "Username: " pocUsername

# Export the environment variables:
export pocUsername=$pocUsername
export pocPassword="password"
export POC_TOKEN=$pocUsername
export POC_GAMESERVER="127.0.0.1"

echo "==============================="
echo "Starting Pirates Online Classic..."
echo "Username: $pocUsername"
echo "Gameserver: $POC_GAMESERVER"
echo "==============================="

ppython -m pirates.piratesbase.PiratesStart
