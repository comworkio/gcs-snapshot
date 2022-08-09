# gcs-snapshot

Google cloud storage snapshot

## Test with docker-compose

1. Generate a service account json key file and place it in the following path: `./service-account-file.json`
2. Generate a `.env` file from the [`.env.example`](./.env.example)

```shell
cp .env.example .env
# change the values inside
```

3. Run docker-compose

```shell
docker-compose up
```
