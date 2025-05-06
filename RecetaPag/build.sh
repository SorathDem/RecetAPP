#!/usr/bin/env bash

cd RecetaPag  # Entra a la carpeta que contiene manage.py
pip install -r ../requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate