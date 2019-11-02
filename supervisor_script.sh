#!/bin/bash

export CV3_PORT=31416
/home/javi/.local/bin/gunicorn --bind 0.0.0.0:$CV3_PORT restapi:app
