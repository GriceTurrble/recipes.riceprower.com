#!/bin/bash

###
# Runs django commands against manage.py within the web container
###

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

THIS_DIR="$(dirname "$(readlink -f "$0")")"
MAIN_DIR="$(dirname $THIS_DIR)"
COMPOSE_FILE=$MAIN_DIR/docker-compose.yml
APP_MANAGE_PY=/app/recipesite/manage.py

docker-compose -f $COMPOSE_FILE exec web poetry run python $APP_MANAGE_PY $@