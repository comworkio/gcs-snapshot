# Gcs Snapshot

Google cloud storage snapshot

## Git repositories

* Main repo: https://gitlab.comwork.io/oss/gcp/gcs-snapshot.git
* Github mirror: https://github.com/idrissneumann/gcs-snapshot.git
* Gitlab mirror: https://gitlab.com/ineumann/gcs-snapshot.git
* Froggit mirror: https://lab.frogg.it/ineumann/gcs-snapshot.git
* Bitbucket mirror: https://bitbucket.org/idrissneumann/gcs-snapshot.git

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
