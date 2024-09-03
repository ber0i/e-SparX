# EDL Registry MVP

This is the repository for the EDL Artifact Registry Project. For details on the project, we refer to to the research proposal "Energy Data Lab: A Machine Learning Artifact Registry for the Energy Transition".

## Getting Started

To start the services, Docker and Docker Compose must be installed. Next, at the root of your project, run

```bash
docker compose --env-file .env up
```

If changes were made, we recommend using the flag `--build` to rebuild the images before starting the containers. If one wants to use the console after starting the containers, one should use the flag  `-d`.

