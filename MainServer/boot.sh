#!/bin/sh
flask kiosk-init-db
# The service announcer now starts in gunicorn post_fork hook defined in gunicorn.conf.py
exec gunicorn -c gunicorn.conf.py neonforge:app