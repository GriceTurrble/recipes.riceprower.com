"""Generates a .env file to use for this project."""

from pathlib import Path
import random
import string
import sys


BASE_DIR = Path(__file__).resolve(strict=True).parent
TEMPLATE = {
    "DEBUG": "on",
    "SECRET_KEY": "__new_secret_key",
    "DATABASE_URL": "__new_sqlite3_url",
    "TIME_ZONE": "US/Eastern",
}
"""Template for building the env file.
Any value starting with `__` will be interpreted as the name of a top-level function
in this module. That function will then be called with no arguments, and the return
value will used as that variable's value in the generated .env file.
"""


def new_secret_key(length=50):
    """Generate a new key to use for Django's SECRET_KEY setting."""
    choice_set = string.ascii_letters + string.digits + "!@#$%^&*(-_+)"
    return "".join([random.SystemRandom().choice(choice_set) for i in range(length)])


def new_sqlite3_url():
    """Returns a new URL for a sqlite3 db at the standard ."""
    url = BASE_DIR / "db.sqlite3"
    return f"sqlite:////{url}"


def main():
    env_filename = BASE_DIR / ".env"
    # if env_filename.exists():
    #     print("ERROR: Env file already exists, and overwriting is not permitted.")
    #     print(
    #         (
    #             "Please make manual changes to the existing file, "
    #             "or remove it before generating a new one."
    #         )
    #     )
    #     sys.exit(1)
    with open(env_filename, "w") as env_file:
        for key, val in TEMPLATE.items():
            if val.startswith("__"):
                func_name = val[2:]
                module = sys.modules[__name__]
                outval = getattr(module, func_name)()
            else:
                outval = val
            env_file.write(f"{key}={outval}\n")


if __name__ == "__main__":
    main()
