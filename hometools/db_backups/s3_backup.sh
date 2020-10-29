#!/bin/bash
# Backs up the database to a file and then uploads it to AWS S3.

source config.sh
# Config fills in:
#   $S3_BUCKET - s3 bucket name, in format `s3://bucket-name`
#   $PG_DATABASE - name of the database to dump, i.e. `mydatabase`

# Dump database backup to a file
TIME=$(date "+%s")
BACKUP_FILE="postgres_${PG_DATABASE}_${TIME}.pgdump"
echo "Backing up $PG_DATABASE to $BACKUP_FILE"
pg_dump --format=custom $PG_DATABASE > $BACKUP_FILE

# Copy file to AWS S3 using awscli
# Don't have awscli? Run `sudo apt-get install awscli` to install,
# then `aws configure` to set credentials. Supply your Access Key
# and Secret Key, then region (us-east-1), and leave default output format.
S3_TARGET=$S3_BUCKET/$BACKUP_FILE
echo "Copying $BACKUP_FILE to $S3_TARGET"
aws s3 cp $BACKUP_FILE $S3_TARGET

echo "Backup completed for $PG_DATABASE"
