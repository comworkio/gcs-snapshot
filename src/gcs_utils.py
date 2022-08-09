from logger_utils import log_msg

def find_or_create_bucket(gcs_client, target_bucket_name):
    try:
        return gcs_client.get_bucket(target_bucket_name)
    except Exception as e:
        log_msg("INFO", "Trying to create bucket {}, e = {}".format(target_bucket, e))
        target_bucket = gcs_client.bucket(target_bucket_name)
        target_bucket.create()
        return target_bucket
