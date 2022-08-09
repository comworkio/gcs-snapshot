from google.cloud import storage
from time import sleep, strftime
from logger_utils import log_msg
from common_utils import is_not_empty
from gcs_utils import find_or_create_bucket, delete_old_buckets

import os
import sys
import datetime

src_bucket_name = os.environ['GCS_SRC_BUCKET_NAME']
wait_time = os.getenv('WAIT_TIME')
retention = int(os.environ['GCS_SNAPSHOT_RETENTION'])
date_format = os.environ['GCS_DEST_DATE_FORMAT']
gcp_project = os.environ['GCP_PROJECT']
add_days_to_current_date = os.getenv('ADD_DAYS_TO_CURRENT_DATE')

gcs_client = storage.Client(project = gcp_project)

while True:
    blobs = gcs_client.list_blobs(src_bucket_name)
    source_bucket = gcs_client.bucket(src_bucket_name)

    current_date = strftime(date_format)
    current_datetime = datetime.datetime.now()
    if is_not_empty(add_days_to_current_date):
        current_datetime = current_datetime + datetime.timedelta(days = int(add_days_to_current_date))

    target_name = "{}-snap-{}".format(src_bucket_name, current_date)
    truncated_name = target_name[-63:]

    delete_old_buckets(current_datetime, truncated_name, gcs_client, date_format, retention)

    target_bucket = find_or_create_bucket(gcs_client, truncated_name)

    for blob in blobs:
        file_name = blob.name
        log_msg("INFO", "[main] copy file {}".format(file_name))
        src_blob = source_bucket.blob(file_name)
        try:
            blob_copy = source_bucket.copy_blob(src_blob, target_bucket, file_name)
        except Exception as e:
            log_msg("ERROR", "[main] unexpected error : {}".format(e))

    if is_not_empty(wait_time):
        log_msg("INFO", "[main] waiting for {}".format(wait_time))
        sleep(int(wait_time))
    else:
        sys.exit()
