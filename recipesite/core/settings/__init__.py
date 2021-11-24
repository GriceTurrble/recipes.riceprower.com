"""Settings for the project.

Most are defined within base, with some defined conditionally within debug and prod.
"""


from .base import *

# DEBUG = bool(os.environ.get("HT_DEBUG", True) == "True")

try:
    from .local_settings import *  # type: ignore
except ImportError:
    pass
