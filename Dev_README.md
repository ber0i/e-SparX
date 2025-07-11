# e-SparX Developer Guide

Welcome to the e-SparX developer README! Here's where you learn what to do to start e-SparX locally and contribute.

## Development

For development, you can launch databases using the `dev.docker-compose.yml`.

As first step, create a `dev.env` file in this directory of the following form:

```bash
MONGO_USER=some_mongo_username
MONGO_PASSWORD=some_mongo_password

POSTGRES_USER=some_postgres_username
POSTGRES_PASSWORD=some_postgres_password

PGADMIN_EMAIL=some@email.com
PGADMIN_PASSWORD=some_pgadmin_password
```

Replace the values with your credentials of choice.

If you're having issues with the default ports or simply want to change them you can do this by setting the following environment variables:

```bash
ARTIFACTDB_GUI_PORT=9081
DAGDB_GUI_PORT=9080
```

For development, the main application (e.g. backend, frontend) have to be setup and launched manually. Refer to the `README.md` file in the corresponding directory. After the setup you can start the docker services.

### Starting the Services

To start the services, Docker and Docker Compose must be installed. Docker Desktop should be run on WSL 2, so in case you are working on a Windows machine, make sure to have WSL 2 installed. Next, at the root of your project, run

```bash
docker compose --env-file dev.env --file dev.docker-compose.yml up
```

In case the docker compose was first started, database migrations must be applied via

```bash
cd backend
alembic upgrade head
```

> Make sure the virtual python environment where you set up the backend is activated.

Whenever changes are made on the SQL database models, a new migration file must be generated via

```bash
cd backend
alembic revision --autogenerate -m "<migration message>"
```

and then again migrated via

```bash
cd backend
alembic upgrade head
```

## Production

The production environment launches all services as containers behind a reverse proxy using the `docker-compose.yml`.

As first step, create a `.env` file in this directory of the following form:

```bash
MONGO_USER=some_mongo_username
MONGO_PASSWORD=some_mongo_password

POSTGRES_USER=some_postgres_username
POSTGRES_PASSWORD=some_postgres_password

PGADMIN_EMAIL=some@email.com
PGADMIN_PASSWORD=some_pgadmin_password
```

Replace the values with your credentials of choice.

If you're having issues with the default ports or simply want to change them you can do this by setting the following environment variables:

```bash
SECURE_SERVER_PORT=8443
SECURE_ARTIFACTDB_GUI_PORT=9443
SECURE_DAGDB_GUI_PORT=10443
```

### SSL Certificates

For security reasons the services can only be accessed over HTTPS.
Make sure to enable HTTPS encrypption, for example, using [Let's Encrypt](https://letsencrypt.org); especially if you're not only experimenting locally for yourself, 
Then set the `ssl_certificate` and `ssl_certificate_key` fields in the proxy config and the proxy container's `volumes` in the docker-compose accordingly.

### Starting the Services

To start the services, Docker and Docker Compose must be installed. Docker Desktop should be run on WSL 2, so in case you are working on a Windows machine, make sure to have WSL 2 installed. Next, at the root of your project, run

```bash
docker compose --env-file .env up
```

If changes were made, we recommend using the flag `--build` to rebuild the images before starting the containers. If one wants to use the console after starting the containers, one should use the flag  `-d`.

In case the docker compose was first started, database migrations must be applied via

```bash
docker exec -it api alembic upgrade head
```

Whenever changes are made on the SQL database models, a new migration file must be generated via

```bash
docker exec -it api alembic revision --autogenerate -m "<migration message>"
```

and then again migrated via

```bash
docker exec -it api alembic upgrade head
```