#!/bin/sh
cd MainServer
sudo rm metadata/*
sudo rm uploads/*
sudo echo '[]' > data/email_queue.json
sudo chmod a+rw instance/site.db
exec ../.venv/bin/python3 -m flask --app neonforge kiosk-reset-db