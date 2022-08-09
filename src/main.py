from google.cloud import storage
from time import sleep, strftime
from logger_utils import log_msg
from common_utils import is_not_empty
from gcs_utils import find_or_create_bucket

import os
import sys

src_bucket_name = os.environ['GCS_SRC_BUCKET_NAME']
wait_time = os.getenv('WAIT_TIME')
retention = int(os.environ['GCS_SNAPSHOT_RETENTION'])
date_format = os.environ['GCS_DEST_DATE_FORMAT']
gcp_project = os.environ['GCP_PROJECT']

gcs_client = storage.Client(project = gcp_project)

while True:
    blobs = gcs_client.list_blobs(src_bucket_name)
    source_bucket = gcs_client.bucket(src_bucket_name)

    vdate = strftime(date_format)
    target_name = "{}-snap-{}".format(src_bucket_name, vdate)
    target_bucket = find_or_create_bucket(gcs_client, target_name[-63:])

    for blob in blobs:
        file_name = blob.name
        log_msg("INFO", "Copy file {}".format(file_name))
        src_blob = source_bucket.blob(file_name)
        try:
            blob_copy = source_bucket.copy_blob(src_blob, target_bucket, file_name)
        except Exception as e:
            log_msg("ERROR", "Unexpected error : {}".format(e))

    if is_not_empty(wait_time):
        log_msg("INFO", "Waiting for {}".format(wait_time))
        sleep(int(wait_time))
    else:
        sys.exit()
