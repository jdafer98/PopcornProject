#!/bin/bash
# /home/travis/.local/bin/gunicorn
export CV3_PORT=31416
sudo /home/travis/virtualenv/python3.6.7/lib/python3.6/site-packages/gunicorn --bind 0.0.0.0:$CV3_PORT restapi:app
