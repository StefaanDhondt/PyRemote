#!/bin/bash

# Change the working dir to make prun find the venv.
cd "$(dirname "$0")"

# Actually start Flask.
sudo prun gunicorn -w 1 -b 0.0.0.0:5000 PyRemote:app