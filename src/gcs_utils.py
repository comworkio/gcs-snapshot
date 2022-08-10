import re

from datetime import datetime
from logger_utils import log_msg

def copy_blobs(gcs_client, src_bucket, target_bucket):
    blobs = gcs_client.list_blobs(src_bucket.name)
    for blob in blobs:
        copy_blob(blob, src_bucket, target_bucket)

def copy_blob(blob, source_bucket, target_bucket):
    file_name = blob.name
    log_msg("INFO", "[copy_blob] copy file {}".format(file_name))
    src_blob = source_bucket.blob(file_name)
    try:
        source_bucket.copy_blob(src_blob, target_bucket, file_name)
    except Exception as e:
        log_msg("ERROR", "[copy_blob] unexpected error : {}".format(e))

def erase_bucket(gcs_client, name):
    blobs = gcs_client.list_blobs(name)
    for blob in blobs:
        log_msg("INFO", "[erase_bucket] deleting {}".format(blob.name))
        blob.delete()

def recreate_bucket(gcs_client, location, name):
    try:
        target_bucket = gcs_client.get_bucket(name)
        try:
            target_bucket.delete(force=True)
        except Exception as de:
            log_msg("INFO", "[recreate_bucket] Refusing to delete the bucket {}, de = {}... removing all files".format(name, de))
            erase_bucket(gcs_client, name)
            target_bucket.delete(force=True)
    except Exception as e:
        log_msg("INFO", "[recreate_bucket] Trying to create bucket {}, e = {}".format(name, e))
    
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
