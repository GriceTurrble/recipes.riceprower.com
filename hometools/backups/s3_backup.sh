#!/bin/bash
# Backs up the database to a file and then uploads it to AWS S3.

CONFIG_FILE=$(dirname $(realpath $0))/config.sh
if [ ! -f "$CONFIG_FILE" ]; then
    echo "Config missing, please make one by copying config.sh.template."
    exit
fi
source $CONFIG_FILE
# Adds:
#   $S3_BUCKET - s3 bucket name, in format `s3://bucket-name`
#   $PG_DATABASE - name of the database to dump, i.e. `mydatabase`
#   $PG_USER - user role to use in the connection

# Dump database backup to a file
TIME=$(date "+%s")
BACKUP_FILE="postgres_${PG_DATABASE}_${TIME}.pgdump"
echo "Backing up $PG_DATABASE to $BACKUP_FILE"
pg_dump --username $PG_USER --format=custom $PG_DATABASE > $BACKUP_FILE

# Copy file to AWS S3 using awscli
# Don't have awscli? Run `sudo apt-get install awscli` to install,
# then `aws configure` to set credentials. Supply your Access Key
# and Secret Key, then region (us-east-1), and leave default output format.
S3_TARGET=$S3_BUCKET/$BACKUP_FILE
echo "Copying $BACKUP_FILE to $S3_TARGET"
aws s3 cp $BACKUP_FILE $S3_TARGET

echo "Backup completed for $PG_DATABASE"
