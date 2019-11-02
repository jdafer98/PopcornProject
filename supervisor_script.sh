#!/bin/bash
# /home/travis/.local/bin/gunicorn
export CV3_PORT=31416
sudo gunicorn --bind 0.0.0.0:$CV3_PORT restapi:app
