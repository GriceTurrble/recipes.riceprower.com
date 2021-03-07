#!/bin/bash

###
# Runs django commands against manage.py within the web container.
# Example:
#   ./django-manage createsuperuser
# Equivalent to:
#   sudo docker-compose -f /path/to/docker-compose.yml exec web poetry run python /app/recipesite/manage.py createsuperuser
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
APP_MANAGE_PY=/app/recipesite/manage.py

exec $THIS_DIR/docker-compose-cmd.sh exec web poetry run python $APP_MANAGE_PY $@
