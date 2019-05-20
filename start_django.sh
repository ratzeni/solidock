#!/bin/bash

#solida info
python solidjango/manage.py migrate --noinput
python solidjango/manage.py runserver 0.0.0.0:8000