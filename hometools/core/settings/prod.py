"""Settings for the production environment only.

Any settings defined here can override base settings implicitly.
"""

from .base import LOGS_ROOT

LOGGING_HANDLERS = {
    # Logs from django.request
    "requests_file": {
        "level": "INFO",
        "filters": ["require_debug_false"],
        "class": "logging.handlers.RotatingFileHandler",
        "maxBytes": 1024 * 1024 * 10,  # 10MB
        "filename": str(LOGS_ROOT / "requests.log"),
        "formatter": "verbose",
    },
    # Logs from django.security
    "security_file": {
        "level": "INFO",
        "filters": ["require_debug_false"],
        "class": "logging.handlers.RotatingFileHandler",
        "maxBytes": 1024 * 1024 * 10,  # 10MB
        "filename": str(LOGS_ROOT / "security.log"),
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
    "null": {
        "class": "logging.NullHandler",
    },
}
LOGGING_LOGGERS = {
    # Catch all in the main log if not configured otherwise
    "django": {
        "handlers": ["file"],
        "propagate": True,
    },
    # Send request access logs to its own file
    "django.request": {
        "handlers": ["requests_file"],
        "level": "INFO",
        "propagate": False,
    },
    # Send security logs to its own file
    "django.security": {
        "handlers": ["security_file"],
        "level": "INFO",
        "propagate": False,
    },
    # Ignore disallowed host errors
    "django.security.DisallowedHost": {
        "handlers": ["null"],
        "propagate": False,
    },
}
