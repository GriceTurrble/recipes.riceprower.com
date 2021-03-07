#!/bin/bash

###
# Runs update tasks for this application.
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

# Update python packages
exec $THIS_DIR/docker-compose-cmd.sh exec web poetry install --no-dev --no-root --no-interaction

# Migrate database changes
exec $THIS_DIR/django-cmd.sh migrate --noinput
# Collect static files
exec $THIS_DIR/django-cmd.sh collectstatic --clear --noinput

# Restart Nginx
systemctl restart nginx
