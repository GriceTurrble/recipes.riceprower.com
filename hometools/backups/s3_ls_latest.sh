#!/bin/bash
source config.sh
# Config fills in:
#   $S3_BUCKET - s3 bucket name, in format `s3://bucket-name`

BACKUP_RESULT=$(aws s3 ls $S3_BUCKET | tail -n 1)
echo "Latest S3 backup: $BACKUP_RESULT"
