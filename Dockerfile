FROM python:3.9-slim-buster

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y gcc procps && \
    apt-get clean

# apt-get installs:
# - gcc to ensure we can install certain Python packages and build from source
# - procps recovers the `ps` command that's missing from the slim build.

# A tutorial I read also recommends `netcat-openbsd`, but I haven't found a use case for it.

# Env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set up working directory
RUN mkdir /app
WORKDIR /app

# Upgrade pip
RUN pip install --upgrade pip

# Install dependencies using poetry
RUN pip install poetry
COPY poetry.lock .
COPY pyproject.toml .
RUN poetry install --no-dev --no-root --no-interaction

# Copy code to the container
RUN mkdir /app/hometools
COPY ./hometools /app/hometools

# Collect static files and run migrations
RUN poetry run python /app/hometools/manage.py collectstatic --clear --noinput
RUN poetry run python /app/hometools/manage.py migrate --noinput

EXPOSE 8000

CMD ["poetry", "run", "python", "/app/hometools/manage.py", "runserver"]