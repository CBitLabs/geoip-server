#!/bin/bash

################################## 
#                                # 
# POSTGRES DUMPS FOR PILOTROI    # 
# Vincent Teyssier               # 
# 19/11/2010                     # 
#                                # 
##################################
#http://open-bi.blogspot.com/2010/11/postgresql-dumps-and-storage-on-s3.html

echo "******************************************************" 
echo "Database dump is starting at : " `date` 
echo "******************************************************"

PG_DUMP=`which pg_dump`

BASE=$1 
SPLITS=$2
DUMP_FILE="/tmp/dumps/$BASE.gz" 
S3ENDPOINT="s3://com.cbitlabs.android/$BASE/"

echo "*****************************" 
echo "Parameters : " 
echo "Base : " $BASE 
echo "Splits : " $SPLITS 
echo "S3 Endpoint : " $S3ENDPOINT 
echo "*****************************"

echo "Dump started at " `date` 
su - postgres -c "$PG_DUMP $BASE | gzip | split -b $SPLITS - $DUMP_FILE" 
echo "Dump ended at " `date` 
echo "*****************************" 
echo "Send to S3 started at " `date` 
s3cmd put $DUMP_FILE* $S3ENDPOINT 
echo "Send ended at " `date` 
echo "*****************************" 
echo "Deleting local dump files" 
yes | rm $DUMP_FILE*

echo "******************************************************" 
echo "Database dump is finished at : " `date` 
echo "******************************************************" 
