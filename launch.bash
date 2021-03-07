#!/bin/bash

# Detects if script are not running as root
if [ "$UID" != "0" ]; then
    if whereis sudo &>/dev/null; then
        # Re-run this script using sudo, then exit
        # $0 is the script itself (or the command used to call it)
        # $@ adds all other arguments
        # The -k option forces the sudo password on every attempt
        # by removing the timeout from any prior sudo call
        # (little extra security)
        exec sudo -k $0 $@
        exit
    else
        echo "Sudo not found. You will need to run this script as root."
        exit
    fi
fi

DIR="$(dirname "$(readlink -f "$0")")"
COMPOSE_FILE=$DIR/docker-compose.yml
APP_MANAGE_PY=/app/recipesite/manage.py

# Bring services up
docker-compose -f $COMPOSE_FILE up

# Update python packages
docker-compose -f $COMPOSE_FILE exec web poetry install --no-dev --no-root --no-interaction
# Migrate database changes
docker-compose -f $COMPOSE_FILE exec web poetry run python $APP_MANAGE_PY migrate --noinput
# Collect static files
docker-compose -f $COMPOSE_FILE exec web poetry run python $APP_MANAGE_PY collectstatic --clear --noinput

# Restart Nginx
systemctl restart nginx
