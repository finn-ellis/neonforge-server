import os
from typing import List, Union
from flask_cors import CORS

def _parse_origins(origins_raw: Union[str, List[str], None]):
    if isinstance(origins_raw, str):
        raw = origins_raw.strip()
        if raw == "*" or raw == "":
            return ["*"]
        return [o.strip() for o in origins_raw.split(',') if o.strip()]
    if isinstance(origins_raw, (list, tuple)):
        return list(origins_raw) or ["*"]
    return ["*"]

def configure_cors(app, *, url_prefix: str, origins_config_key: str, creds_config_key: str):
    """Apply consistent CORS setup for an extension namespace.

    Environment variables with the same names as the config keys override defaults.
    - origins_config_key: e.g. FILESERVER_CORS_ORIGINS, KIOSK_QUEUE_CORS_ORIGINS
    - creds_config_key: e.g. FILESERVER_CORS_SUPPORTS_CREDENTIALS
    """
    # Allow env var overrides (Flask doesn't auto-load arbitrary env vars)
    if origins_config_key in os.environ:
        app.config[origins_config_key] = os.environ[origins_config_key]
    if creds_config_key in os.environ:
        val = os.environ[creds_config_key].lower()
        app.config[creds_config_key] = val in ("1", "true", "yes", "on")

    origins_list = _parse_origins(app.config.get(origins_config_key, "*"))
    supports_creds = bool(app.config.get(creds_config_key, False))

    print(f"Configuring CORS for {url_prefix} with origins: {origins_list}, supports_credentials={supports_creds}")
    resources = {
        f"{url_prefix}/*": {"origins": origins_list},
        "/socket.io/*": {"origins": origins_list},
    }
    CORS(app, resources=resources, supports_credentials=supports_creds)
    return origins_list

__all__ = ["configure_cors"]