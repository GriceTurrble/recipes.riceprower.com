"""Settings for the debug environment only.

Any settings defined here can override base settings implicitly.
"""

from .base import *
from .base import LOGGING, LOGS_DIR

# Logging handlers and loggers are imported direct in settings.__init__.
# These are not standard settings, but we're using these to define the logging setup
# relevant to this environment
LOGGING["handlers"] = {
    # Set up a console handler to show INFO in the terminal
    "console": {
        "level": "INFO",
        "filters": ["require_debug_true"],
        "class": "logging.StreamHandler",
        "formatter": "simple",
    },
    # Debug file that can log basically anything
    # Attempt to make a rotating file, though it won't rotate properly
    # unless `runsever --no-reload` is set.
    "debug_file": {
        "level": "DEBUG",
        "filters": ["require_debug_true"],
        "class": "logging.handlers.RotatingFileHandler",
        "filename": str(LOGS_DIR / "debug.log"),
        "maxBytes": 1024 * 1024 * 10,  # 10MB
        "backupCount": 10,
        "formatter": "verbose",
    },
}
LOGGING["loggers"] = {
    # Send general messages to console and the debug file
    "django": {
        "handlers": ["console", "debug_file"],
        "propagate": True,
    },
    # Database debug messages to file
    "django.db.backends": {
        "handlers": ["debug_file"],
        "level": "DEBUG",
        "propagate": False,
    },
}
