"""Settings for the production environment only.

Any settings defined here can override base settings implicitly.
"""

from .base import LOGS_ROOT

LOGGING_HANDLERS = {
    # Security warnings logging
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
        "filename": str(LOGS_ROOT / "django.log"),
        "formatter": "verbose",
    },
    "null": {
        "class": "logging.NullHandler",
    },
}
LOGGING_LOGGERS = {
    # Catch all in the main log
    "django": {
        "handlers": ["file"],
        "propagate": True,
    },
    # Capture security logs
    "django.security": {
        "handlers": ["security_file"],
        "level": "INFO",
        "propagate": False,
    },
    # Ignore DisallowedHost errors
    "django.security.DisallowedHost": {
        "handlers": ["null"],
        "propagate": False,
    },
}
