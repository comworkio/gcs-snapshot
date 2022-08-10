from google.cloud import storage
from time import sleep, strftime
from logger_utils import log_msg
from common_utils import is_not_empty
from gcs_utils import recreate_bucket, delete_old_buckets, copy_blobs

import os
import sys
import datetime

src_bucket_name = os.environ['GCS_SRC_BUCKET_NAME']
wait_time = os.getenv('WAIT_TIME')
retention = int(os.environ['GCS_SNAPSHOT_RETENTION'])
date_format = os.environ['GCS_DEST_DATE_FORMAT']
gcp_project = os.environ['GCP_PROJECT']
location = os.environ['GCS_LOCATION']
add_days_to_current_date = os.getenv('ADD_DAYS_TO_CURRENT_DATE')
snapshot_to_restore = os.getenv('SNAPSHOT_TO_RESTORE')

gcs_client = storage.Client(project = gcp_project)

if is_not_empty(snapshot_to_restore):
    log_msg("INFO", "Restore {} to {}".format(snapshot_to_restore, src_bucket_name))
    snapshot_bucket = gcs_client.bucket(snapshot_to_restore)
    target_bucket = recreate_bucket(gcs_client, location, src_bucket_name)
    copy_blobs(gcs_client, snapshot_bucket, target_bucket)
    sys.exit()

while True:
    source_bucket = gcs_client.bucket(src_bucket_name)
    current_date = strftime(date_format)
    current_datetime = datetime.datetime.now()
    if is_not_empty(add_days_to_current_date):
        current_datetime = current_datetime + datetime.timedelta(days = int(add_days_to_current_date))

    target_name = "{}-snap-{}".format(src_bucket_name, current_date)
    truncated_name = target_name[-63:]

    delete_old_buckets(current_datetime, truncated_name, gcs_client, date_format, retention)

    target_bucket = recreate_bucket(gcs_client, location, truncated_name)

    copy_blobs(gcs_client, source_bucket, target_bucket)

    if is_not_empty(wait_time):
        log_msg("INFO", "[main] waiting for {}".format(wait_time))
        sleep(int(wait_time))
    else:
        sys.exit()
