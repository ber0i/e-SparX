# e-SparX - Backend

This is the e-SparX backend based on [FastAPI](https://fastapi.tiangolo.com).

## Getting Started

As first step, create a `.env` file in this directory of the following form:

```bash
ARTIFACTDB_ENDPOINT="<MONGO_USER>:<MONGO_PASSWORD>@localhost:27017"
DAGDB_CONNECTSTRING="postgresql://<POSTGRES_USER>:<POSTGRES_PASSWORD>@localhost:5432/dagdb"
```

Replace `MONGO/POSTGRES_USER` and `MONGO/POSTGRES_PASSWORD` with your credentials of choice you used in the `.env` file in the project's root directory.

Next, install all dependencies. For this, create a new virtual environment (use Python version 3.12), activate the environment and then run:

```bash
pip install -e ".[dev]"
```

For managing your virtual environments, you can use [Miniconda](https://docs.anaconda.com/free/miniconda/index.html), for example. For more information of how to create and manage virtual python environments, see [here](https://conda.io/projects/conda/en/latest/user-guide/getting-started.html).

After installing all dependencies as described above, you can start the API as follows:

```bash
esparx-api --reload
```

The `--reload` flag is optional and is recommended during development.

The API is now running on [http://localhost:8080](http://localhost:8080).

When running the entire project with docker compose, the backend will run in the api container.

## Database Migrations

The PostgresSQL database requires migration scripts to be created and run. Whenever a change is made on the database structure, the corrsponding migration scripts can be created automatically via running
```bash
alembic revision --autogenerate -m "<migration message>"
```
Replace `<migration message>` with a short description of the changes you applied. Migrations are executed via
```bash
alembic upgrade head
```

