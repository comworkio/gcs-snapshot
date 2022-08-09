import re

from datetime import datetime
from logger_utils import log_msg

def find_or_create_bucket(gcs_client, location, name):
    try:
        target_bucket = gcs_client.get_bucket(name)
        target_bucket.delete(force=True)
    except Exception as e:
        log_msg("INFO", "[find_or_create_bucket] Trying to create bucket {}, e = {}".format(name, e))
    
    target_bucket = gcs_client.bucket(name)
    target_bucket.create(location = location)
    return target_bucket

def delete_old_buckets(current_date, target_name, gcs_client, date_format, retention):
    prefix = re.sub("-snap-[0-9]+$", '', target_name)
    for bucket in gcs_client.list_buckets(prefix = prefix):
        bucket_name = bucket.name
        creation_date = datetime.strptime(bucket_name, "{}-snap-{}".format(prefix, date_format))
        d = (current_date - creation_date).days
        if d >= retention:
            log_msg("INFO", "[delete_old_buckets] delete bucket {} because d = {} >= r = {}".format(bucket.name, d, retention))
            bucket.delete(force=True)
