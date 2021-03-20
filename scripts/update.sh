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

echo ">> Bringing services down"
. $THIS_DIR/stop.sh

echo ">> Rebuilding images"
. $THIS_DIR/rebuild-images.sh

echo ">> Updating python packages"
. $THIS_DIR/docker-compose-cmd.sh exec web poetry install --no-dev --no-root --no-interaction

echo ">> Migrating database changes"
. $THIS_DIR/django-cmd.sh migrate --noinput

echo ">> Collecting static files"
. $THIS_DIR/django-cmd.sh collectstatic --clear --noinput

echo ">> Restarting Nginx"
systemctl restart nginx

echo ">> Bringing services up"
. $THIS_DIR/start.sh

echo ">> Update complete. Check the live site now!"
