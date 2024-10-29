# EDL Registry MVP

This is the repository for the EDL Artifact Registry Project. For details on the project, we refer to to the research proposal "Energy Data Lab: A Machine Learning Artifact Registry for the Energy Transition".

## Getting Started

As first step, create a `.env` file in this directory of the following form:

```bash
MONGO_USER=some_mongo_username
MONGO_PASSWORD=some_mongo_password
POSTGRES_USER=some_postgres_username
POSTGRES_PASSWORD=some_postgres_password
PGADMIN_EMAIL=some@email.com
PGADMIN_PASSWORD=some_pgadmin_password
APP_DOMAIN=http://puplic_ip_address_or_domain_of_the_server
```

Replace the values with your credentials of choice.

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