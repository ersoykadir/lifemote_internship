#!/bin/bash

# Abort on any error (including if wait-for-it fails).
set -e

# Wait for the backend to be up, if we know where it is.
if [ -n "$SERVER_HOST" ]; then
  ./wait-for-it.sh $SERVER_HOST:$SERVER_PORT
fi

# Run the main container command.
python main.py