#!/bin/bash

###
# Rebuilds NPM styles
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

. $THIS_DIR/docker-compose-cmd.sh exec web bash -c "cd /app/recipesite/assets && NODE_ENV=production npm run build"
