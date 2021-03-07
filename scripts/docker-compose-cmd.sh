#!/bin/bash

###
# Shorthand for running arbitary commands in docker-compose for this application.
# Given this project contains an override file intended for development,
# speciying the production config is required. This script simply adds the argument
# for that config file automatically.
# Example:
#   ./docker-compose-cmd.sh ps
# Equivalent to:
#   sudo docker-compose -f /path/to/docker-compose.yml ps
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

docker-compose -f $COMPOSE_FILE $@
