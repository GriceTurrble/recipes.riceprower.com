#!/bin/bash
# Restores latest backup stored in our S3 backups bucket

source config.sh
# Config fills in:
#   $S3_BUCKET - s3 bucket name, in format `s3://bucket-name`
#   $PG_DATABASE - name of the database to dump, i.e. `mydatabase`
#   $PG_USER - user that will connect to make the backup.

echo -e "\nRestoring database $PG_DATABASE from S3 backups"

# Find the latest backup file
LATEST_FILE=$(aws s3 ls $S3_BUCKET | awk '{print $4}' | sort | tail -n 1)
echo -e "\nFound file $LATEST_FILE in bucket $S3_BUCKET"

# Restore from the latest backup file
echo -e "\nRestoring $PG_DATABASE from $LATEST_FILE"
S3_TARGET=$S3_BUCKET/$LATEST_FILE
aws s3 cp $S3_TARGET - | pg_restore --username $PG_USER --no-password --dbname $PG_DATABASE --clean --no-owner
echo -e "\nRestore completed"
