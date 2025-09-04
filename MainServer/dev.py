import eventlet
from eventlet import wsgi
import atexit
import sys
import threading
from flask import Flask
import os
from flask_socketio import SocketIO
from FileServer.file_server import FileServer
from FileServer.file_server.service_announcer import ServiceAnnouncer
from flask import Flask
from KioskQueue.kiosk_queue import KioskQueue
from KioskQueue.kiosk_queue.config import Config
import click
from flask import current_app

from neonforge import create_app

app = create_app()