"""Settings for the project.

Most are defined within base, with some defined conditionally within debug and prod.
"""

from .base import env
from .base import *

DEBUG = env.bool("DEBUG")

if DEBUG:
    from .dev import *
else:
    from .prod import *
try:
    # Attempt to pull settings overrides from a local file, if any is present
    from .local import *  # type: ignore
except ImportError:
    pass


# Do not attempt to define LOGGING in any of the environments above,
# as the definition below will simply overwrite it.
# Instead, use these `LOGGING_foo` constants to change different pieces of the config.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": LOGGING_FORMATTERS,  # noqa
    "filters": LOGGING_FILTERS,  # noqa
    "handlers": LOGGING_HANDLERS,  # noqa
    "loggers": LOGGING_LOGGERS,  # noqa
}
