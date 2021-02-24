"""Settings for the production environment only.

Any settings defined here can override base settings implicitly.
"""

from .base import *
from .base import LOGGING, LOGS_DIR

LOGGING["root"] = {
    "handlers": ["file"],
    "level": "INFO",
}
LOGGING["handlers"] = {
    # Security warnings logging
    "security_file": {
        "level": "INFO",
        "filters": ["require_debug_false"],
        "class": "logging.handlers.RotatingFileHandler",
        "maxBytes": 1024 * 1024 * 10,  # 10MB
        "backupCount": 10,
        "filename": str(LOGS_DIR / "security.log"),
        "formatter": "verbose",
    },
    # Other general INFO messages in a main log
    "file": {
        "level": "INFO",
        "filters": ["require_debug_false"],
        "class": "logging.handlers.RotatingFileHandler",
        "maxBytes": 1024 * 1024 * 10,  # 10MB
        "backupCount": 10,
        "filename": str(LOGS_DIR / "django.log"),
        "formatter": "verbose",
    },
    "null": {
        "class": "logging.NullHandler",
    },
}
LOGGING["loggers"] = {
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


# Additional security settings
SECURE_HSTS_SECONDS = 3600
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
