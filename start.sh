#!/usr/bin/env bash

# Check for the setup lock
FILENAME="setup.lock"
 
if [ ! -f "$FILENAME" ]
then
  echo "$FILENAME not found - running setup..."
  ./setup.sh
fi 

# Ensure all prints make it to the journal log
export PYTHONUNBUFFERED=true

# Start the onvif ptz adapter
bash -c "uvicorn main:app --reload --host 0.0.0.0 --ssl-keyfile=./server.key --ssl-certfile=./server.crt"