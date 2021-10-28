"""Settings for the project.

Most are defined within base, with some defined conditionally within debug and prod.
"""

# import os

# from .base import env
from .base import *

# DEBUG = bool(os.environ.get("HT_DEBUG", True) == "True")

try:
    from .local import *  # type: ignore
except ImportError:
    pass
    # if DEBUG:
    #     from .dev import *
    # else:
    #     from .prod import *
