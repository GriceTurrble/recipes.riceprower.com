"""Settings for the production environment only.

Any settings defined here can override base settings implicitly.
"""

from .base import LOGS_ROOT

LOGGING_HANDLERS = {
    # Server access logs from django.request
    "access_file": {
        "level": "INFO",
        "filters": ["require_debug_false"],
        "class": "logging.handlers.RotatingFileHandler",
        "maxBytes": 1024 * 1024 * 10,  # 10MB
        "filename": str(LOGS_ROOT / "access.log"),
        "formatter": "verbose",
    },
    # Other general INFO messages in a main log
    "file": {
        "level": "INFO",
        "filters": ["require_debug_false"],
        "class": "logging.handlers.RotatingFileHandler",
        "maxBytes": 1024 * 1024 * 10,  # 10MB
        "filename": str(LOGS_ROOT / "main.log"),
        "formatter": "verbose",
    },
}
LOGGING_LOGGERS = {
    # Catch all in the main log if not configured otherwise
    "django": {
        "handlers": ["file"],
        "propagate": True,
    },
    # Send server access logs to its own file
    "django.server": {
        "handlers": ["access_file"],
        "level": "ERROR",
        "propagate": False,
    },
    # Only show ERROR messages from the request logger in main log
    "django.request": {
        "handlers": ["file"],
        "level": "ERROR",
        "propagate": False,
    },
}
