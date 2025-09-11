import os
import socket

from zeroconf import Zeroconf, ServiceInfo

# Gunicorn configuration file.
# We use gevent worker for SocketIO compatibility.
worker_class = 'gevent'
workers = 1
bind = ":80"

# Ensure graceful shutdowns
graceful_timeout = 30

# Logging - inherit stdout/stderr so docker logs show them.
accesslog = '-'  # stdout
errorlog = '-'   # stderr
loglevel = os.environ.get('GUNICORN_LOG_LEVEL', 'info')

# Zeroconf instance, will be created in the when_ready hook
zc = None
# Service info, will be created in the when_ready hook
service_info = None

def when_ready(server):
    """Called in the worker process after initialization."""
    global zc, service_info

    server.log.info("Gunicorn is ready. Starting service announcer...")
    try:
        # from neonforge import start_service_announcer
        # start_service_announcer()
        server.log.info("Service announcer started.")
        addr = socket.gethostbyname(socket.gethostname())
        port = 80 #hardcoded bad
        service_type = "_http._tcp.local."
        service_name = "NF"
        full_qualified_name = f"{service_name}.{service_type}"
        service_info = ServiceInfo(
            service_type,
            full_qualified_name,
            addresses=[socket.inet_aton(addr)],
            port=port,
            properties={'description': 'NeonForge File Server.'},
        )

        zeroconf = Zeroconf()
        zeroconf.register_service(service_info)
        server.log.info(f"Zeroconf service '{full_qualified_name}' registered on {addr}:{port}.")
        # output no work:
        # from FileServer.file_server.test_service_announcer import test
        # test()
    except Exception as e:
        server.log.error('Failed to start service announcer: %s', e)

def on_exit(server):
    """
    Called just before exiting Gunicorn.
    Unregister the Zeroconf service here.
    """
    global zc, service_info
    if zc and service_info:
        server.log.info(f"Unregistering Zeroconf service.")
        zc.unregister_service(service_info)
        zc.close()
