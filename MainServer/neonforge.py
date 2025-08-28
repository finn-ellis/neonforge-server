import eventlet
# eventlet.monkey_patch()

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

@click.command("initialize-server")
def init_server_command():
    start_service_announcer()
    click.echo("Service announced!")

def create_app():
    global announcer_started
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    # Allow unified CORS env overrides prior to extension init
    # Users can set (comma-separated): FILESERVER_CORS_ORIGINS, KIOSK_QUEUE_CORS_ORIGINS
    # And booleans: FILESERVER_CORS_SUPPORTS_CREDENTIALS, KIOSK_QUEUE_CORS_SUPPORTS_CREDENTIALS
    def _bool(env_key, default=False):
        val = os.environ.get(env_key)
        if val is None:
            return default
        return val.lower() in ("1", "true", "yes", "on")

    if "FILESERVER_CORS_ORIGINS" in os.environ:
        app.config["FILESERVER_CORS_ORIGINS"] = os.environ["FILESERVER_CORS_ORIGINS"]
    if "KIOSK_QUEUE_CORS_ORIGINS" in os.environ:
        app.config["KIOSK_QUEUE_CORS_ORIGINS"] = os.environ["KIOSK_QUEUE_CORS_ORIGINS"]
    if "FILESERVER_CORS_SUPPORTS_CREDENTIALS" in os.environ:
        app.config["FILESERVER_CORS_SUPPORTS_CREDENTIALS"] = _bool("FILESERVER_CORS_SUPPORTS_CREDENTIALS")
    if "KIOSK_QUEUE_CORS_SUPPORTS_CREDENTIALS" in os.environ:
        app.config["KIOSK_QUEUE_CORS_SUPPORTS_CREDENTIALS"] = _bool("KIOSK_QUEUE_CORS_SUPPORTS_CREDENTIALS")

    file_server.init_app(app, url_prefix="/api/files", socketio=socketio)
    kiosk.init_app(app, url_prefix="/api/kiosk", socketio=socketio)
    socketio.init_app(app)

    app.cli.add_command(init_server_command)

    # how do we only do this when the app is ran??? and not for CLI commands?
    # TODO: change this with prod implementation
    # def start_announcer_once():
    #     global announcer_started
    #     if not announcer_started:
    #         start_service_announcer()
    #         announcer_started = True
    
    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
