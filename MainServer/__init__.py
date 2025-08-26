import atexit
import sys
import threading
from flask import Flask
from flask_socketio import SocketIO
from FileServer.file_server import FileServer
from FileServer.file_server.service_announcer import ServiceAnnouncer
from flask import Flask
from .KioskQueue.kiosk_queue import KioskQueue
from .KioskQueue.kiosk_queue.config import Config

socketio = SocketIO(cors_allowed_origins="*")
kiosk = KioskQueue()
file_server = FileServer()

def start_service_announcer():
    """Starts the Zeroconf service announcer in a background thread."""
    print("Starting service announcer...")
    service_type = "_file-server._tcp.local."
    service_name = "NF"
    server_port = 5000  # Default Flask port

    announcer = ServiceAnnouncer(service_type, service_name, server_port)

    # Run the service announcer in a background thread
    announcer_thread = threading.Thread(target=announcer.start, daemon=True)
    announcer_thread.start()

    # Register the stop function to be called on exit
    atexit.register(announcer.stop)

announcer_started = False

def create_app():
    global announcer_started
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    file_server.init_app(app, url_prefix="/api/files", socketio=socketio)
    kiosk.init_app(app, url_prefix="/api/kiosk", socketio=socketio)
    socketio.init_app(app)

    # how do we only do this when the app is ran??? and not for CLI commands?
    # TODO: change this with prod implementation
    def start_announcer_once():
        global announcer_started
        if not announcer_started:
            start_service_announcer()
            announcer_started = True
    
    start_announcer_once()
    
    return app

app = create_app()
