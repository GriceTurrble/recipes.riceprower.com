ARG APP_DIR=recipesite


# ---------------------------------------------------------------------------------------
# Building static assets from Node
FROM node:18-bullseye-slim AS node-assets
ARG APP_DIR

# Update system packages as needed (security measure)
# Periodically rebuild image with `docker build --pull --no-cache` to ensure updates
RUN apt-get update && \
    apt-get upgrade -y

COPY js_toolchain /code/js_toolchain
COPY $APP_DIR /code/$APP_DIR
WORKDIR /code/js_toolchain
RUN npm ci
RUN npm run build:prod
# This creates assets we'll find at -> /code/$APP_DIR/static/
# (see js_toolchain/package.json for details)


# ---------------------------------------------------------------------------------------
# Customize our python base image in-flight
FROM python:3.10-slim-bullseye AS python-base

# Update system packages as needed (security measure)
# Periodically rebuild image with `docker build --pull --no-cache` to ensure updates
RUN apt-get update && \
    apt-get upgrade -y

# Upgrade pip to latest
RUN python -m pip install --upgrade pip


# ---------------------------------------------------------------------------------------
# Generate workable requirements.txt from Poetry dependencies
FROM python-base as requirements

# Dependencies for Poetry to operate
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    gcc

# Install poetry from PyPI
RUN python -m pip install --no-cache-dir --upgrade poetry

# Generate `requirements.txt`, which we'll copy later
COPY pyproject.toml poetry.lock ./
RUN poetry export --format=requirements.txt --output=requirements.txt && \
    poetry export --without-hashes --dev --format=requirements.txt --output=requirements-dev.txt


# ---------------------------------------------------------------------------------------
# Switch to non-root user appuser
# This can't be done in the base image for requirements,
# as apt-get is still needed from root
FROM python-base as appuser-base

RUN adduser appuser
WORKDIR /home/appuser
USER appuser:appuser

ENV PATH /home/appuser/.local/bin:$PATH


# ---------------------------------------------------------------------------------------
# Development image
FROM appuser-base as development
ARG APP_DIR

# Install requirements
COPY --from=requirements requirements-dev.txt /home/appuser/requirements.txt
RUN pip install --no-cache-dir --user -r /home/appuser/requirements.txt

# Site code
COPY $APP_DIR/ /home/appuser/$APP_DIR/
# Generated static files
COPY --from=node-assets /code/$APP_DIR/static/ /home/appuser/$APP_DIR/static/
# Gunicorn config file
COPY gunicorn.conf.py /home/appuser/gunicorn.conf.py

# Change to directory containing manage.py (for running management commands more easily)
WORKDIR /home/appuser/$APP_DIR

# Start with gunicorn, configured via our config file.
CMD ["python", "-m", "gunicorn", "-c", "/home/appuser/gunicorn.conf.py", "core.asgi:application"]



# ---------------------------------------------------------------------------------------
# Production image
FROM appuser-base as production
ARG APP_DIR

# Install requirements
COPY --from=requirements requirements.txt /home/appuser/requirements.txt
RUN pip install --no-cache-dir --user -r /home/appuser/requirements.txt

# Site code
COPY $APP_DIR/ /home/appuser/$APP_DIR/
# Generated static files
COPY --from=node-assets /code/$APP_DIR/static/ /home/appuser/$APP_DIR/static/
# Gunicorn config file
COPY gunicorn.conf.py /home/appuser/gunicorn.conf.py

# Change to directory containing manage.py (for running management commands more easily)
WORKDIR /home/appuser/$APP_DIR

# Start with gunicorn, configured via our config file.
CMD ["python", "-m", "gunicorn", "-c", "/home/appuser/gunicorn.conf.py", "core.asgi:application"]
