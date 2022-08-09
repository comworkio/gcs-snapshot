from logger_utils import log_msg

def find_or_create_bucket(gcs_client, name):
    try:
        return gcs_client.get_bucket(name)
    except Exception as e:
        log_msg("INFO", "Trying to create bucket {}, e = {}".format(name, e))
        target_bucket = gcs_client.bucket(name)
        target_bucket.create()
        return target_bucket
