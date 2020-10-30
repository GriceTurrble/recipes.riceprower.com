#!/bin/bash

CONFIG_FILE=$(dirname $(realpath $0))/config.sh
if [ ! -f "$CONFIG_FILE" ]; then
    echo "Config missing, please make one by copying config.sh.template."
    exit
fi
source $CONFIG_FILE
# Adds:
#   $S3_BUCKET - s3 bucket name, in format `s3://bucket-name`

BACKUP_RESULT=$(aws s3 ls $S3_BUCKET | tail -n 1)
echo "Latest S3 backup: $BACKUP_RESULT"
