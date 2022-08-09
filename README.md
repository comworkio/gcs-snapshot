# Gcs Snapshot

Google cloud storage snapshot

## Git repositories

* Main repo: https://gitlab.comwork.io/oss/gcp/gcs-snapshot.git
* Github mirror: https://github.com/idrissneumann/gcs-snapshot.git
* Gitlab mirror: https://gitlab.com/ineumann/gcs-snapshot.git
* Froggit mirror: https://lab.frogg.it/ineumann/gcs-snapshot.git
* Bitbucket mirror: https://bitbucket.org/idrissneumann/gcs-snapshot.git

## Environment variables

* `GCP_PROJECT` (required): gcp project
* `GCS_SRC_BUCKET_NAME` (required): the source bucket you want to snapshot
* `GCS_DEST_BUCKET_PREFIX` (required): the destination bucket prefix (it'll be concatenate with the current date)
* `GCS_SNAPSHOT_RETENTION` (required): the number of snapshot to keep
* `GCS_DEST_DATE_FORMAT` (optional): the date format (default: `%Y%m%d`)
* `WAIT_TIME` (optional): if you want the pod to stay alive like a service worker, it will wait this time (in seconds). Otherwise, it'll `exit 0` in order to allow you to use the image in a cron job or a pipeline/workflow using something else.
* `LOG_LEVEL` (optional): log level, default `INFO`
* `GOOGLE_APPLICATION_CREDENTIALS` (optional): path the the service account json file (to mount as a volume). No need when you're using Kubernetes cloud identity

## Test with docker-compose

1. Generate a service account json key file and place it in the following path: `./service-account-file.json`
2. Generate a `.env` file from the [`.env.example`](./.env.example)

```shell
cp .env.example .env
# change the values inside
```

3. Run docker-compose

```shell
docker-compose up --build --force-recreate
```
