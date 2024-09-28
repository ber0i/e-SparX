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
```

Replace the values with your credentials of choice.

To start the services, Docker and Docker Compose must be installed. Next, at the root of your project, run

```bash
docker compose --env-file .env up
```

If changes were made, we recommend using the flag `--build` to rebuild the images before starting the containers. If one wants to use the console after starting the containers, one should use the flag  `-d`.

Currently, the frontend is not integrated in the docker compose. Must be started manually. See the README file in the frontend folder on how to do this.
