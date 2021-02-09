#!/bin/sh

python3 manage.py db upgrade
python3 app.py