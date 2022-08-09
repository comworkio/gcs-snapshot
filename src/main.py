from google.cloud import storage
from time import sleep
from logger_utils import log_msg
from common_utils import is_not_empty

import os
import sys

gcs_client = storage.Client()
src_bucket_name = os.environ['GCS_SRC_BUCKET_NAME']
dest_bucket_prefix = os.environ['GCS_DEST_BUCKET_PREFIX']
wait_time = os.getenv('WAIT_TIME')

while True:
    blobs = gcs_client.list_blobs(src_bucket_name)

    for blob in blobs:
        print(blob.name)
    
    if is_not_empty(wait_time):
        log_msg("INFO", "Waiting for {}".format(wait_time))
        sleep(int(wait_time))
    else:
        sys.exit()
