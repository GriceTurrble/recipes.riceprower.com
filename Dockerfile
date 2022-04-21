# Building static assets from Node
FROM node:18-bullseye-slim AS node-assets

# Update system packages as needed (security measure)
# Periodically rebuild image with `docker build --pull --no-cache` to ensure updates
RUN apt-get update && \
    apt-get upgrade -y

COPY js_toolchain /code/js_toolchain
COPY recipesite /code/recipesite
WORKDIR /code/js_toolchain
RUN npm ci
RUN npm run build:prod
# This creates assets we'll find at -> /django_app/static/

# ---------------------------------------------------------------------------------------------------------------------
# Customize our python base image in-flight
FROM python:3.10-slim-bullseye AS python-base
RUN apt-get update && \
    apt-get upgrade -y
RUN python -m pip install --upgrade pip

# ---------------------------------------------------------------------------------------------------------------------
# Generate workable requirements.txt from Poetry dependencies
FROM python-base as requirements

RUN apt-get install -y --no-install-recommends build-essential gcc
RUN python -m pip install --no-cache-dir --upgrade poetry

WORKDIR /src
COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt --without-hashes -o /src/requirements.txt

# ---------------------------------------------------------------------------------------------------------------------
# Final app image
FROM python-base as webapp

# Switching to non-root user appuser
RUN adduser appuser
WORKDIR /home/appuser
USER appuser:appuser

# Install requirements
COPY --from=requirements /src/requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt
# Site code
COPY recipesite/ /home/appuser/recipesite/
# Generated static files from node-assets layer
COPY --from=node-assets /code/recipesite/static/ /home/appuser/recipesite/static/
# Gunicorn config file
COPY gunicorn.conf.py /home/appuser/gunicorn.conf.py
RUN echo $PATH

# Change to directory containing manage.py (for running management commands more easily)
WORKDIR /home/appuser/recipesite

# Start with gunicorn, configured via our config file.
CMD ["python", "-m", "gunicorn", "-c", "/home/appuser/gunicorn.conf.py", "core.asgi:application"]
