# EDL Backend

This is the Backend for the Energy Data Lab based on [FastAPI](https://fastapi.tiangolo.com).

## Getting Started

First, install all dependencies. For this, create a new virtual environment, activate the environment and then run:

```bash
pip install -e ".[dev]"
```

For managing your virtual environments, you can use [Miniconda](https://docs.anaconda.com/free/miniconda/index.html), for example. For more information of how to create and manage virtual python environments, see [here](https://conda.io/projects/conda/en/latest/user-guide/getting-started.html).

After installing all dependencies as described above, you can start the API as follows:

```bash
edl-api --reload
```

The `--reload` flag is optional and is recommended during development.

The API is now running on [http://localhost:8000](http://localhost:8000).