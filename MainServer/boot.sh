#!/bin/sh
flask kiosk-init-db
flask initialize-server
exec gunicorn --worker-class eventlet -w 1 -b :5000 neonforge:app