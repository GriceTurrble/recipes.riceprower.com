#!/bin/bash

# Force sudo if not set
[ "$UID" -eq 0 ] || exec sudo bash "$0" "$@"

CONFIG_FILE=$(realpath config.sh)

if [ -f "$CONFIG_FILE" ]; then
    echo "Config missing, please make one by copying config.sh.template."
    exit
fi

source $CONFIG_FILE
# Adds:
#   $MANAGE_DIR - full path to directory where manage.py can be found
#   $ENV_ACTIVATE - path to the "activate" script for the venv for the project

cd $MANAGE_DIR

echo "[DEPLOY] pulling changes from Git remote..."
git checkout -f main
git pull

echo "[DEPLOY] Activating venv..."
source $ENV_ACTIVATE
echo "[DEPLOY] Collecting static files..."
python manage.py collectstatic --clear --noinput
echo "[DEPLOY] Migrating DB changes..."
python manage.py migrate --noinput
echo "[DEPLOY] Deactivating venv..."
deactivate

echo "[DEPLOY] Restarting services..."
systemctl daemon-reload
systemctl restart gunicorn
systemctl restart nginx
echo "[DEPLOY] Complete."
