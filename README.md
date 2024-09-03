# EDL Registry MVP

This is the repository for the EDL Artifact Registry Project. For details on the project, we refer to to the research proposal "Energy Data Lab: A Machine Learning Artifact Registry for the Energy Transition".

## Getting Started

As first step, create a `.env` file in this directory of the following form:

```bash
MONGO_USER=some_username
MONGO_PASSWORD=some_password
```

Replace `some_username` and `some_password` with your credentials of choice.

To start the services, Docker and Docker Compose must be installed. Next, at the root of your project, run

```bash
docker compose --env-file .env up
```

If changes were made, we recommend using the flag `--build` to rebuild the images before starting the containers. If one wants to use the console after starting the containers, one should use the flag  `-d`.

## DocumentDB

To inspect the content of the MongoDB, where the JSON files are stored, one can install MongoDB Compass. To connect to the DB running inside the edl-documentb container, use the following connection string (you will be asked for this after opening MongoDB Compass):

```bash
mongodb://<MONGO_USER>:<MONGO_PASSWORD>@localhost:27017
```
