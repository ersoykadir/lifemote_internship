#!/bin/bash

# Abort on any error (including if wait-for-it fails).
set -e

# Wait for the backend to be up, if we know where it is.
if [ -n "$MYSQL_HOST" ]; then
  ./wait-for-it.sh $MYSQL_HOST:3306
fi

# Run the main container command.
alembic upgrade head
python main.py