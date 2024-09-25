# PyDocker
A simple Python Docker workspace template for developing Python projects within Docker containers.

## Usage

1. Start the development environment with:

    ```bash
    $ docker-compose up -d

    => => naming to docker.io/library/pydocker-workspace                                                                       0.0s 
    [+] Running 2/2
    ✔ Network pydocker_default     Created                                                                                     0.1s 
    ✔ Container python-playground  Started 
    ```

2. Access docker container terminal with:

    ```bash
    $ docker exec -it python-playground /bin/bash

    # OUTPUT
    # root@46a62809e109:/code
    ```

    Exit terminal with `CTRL + D`.

3. Stop docker container with:

    ```bash
    $ docker compose down

    PS D:\github\PyDocker> docker compose down
    [+] Running 2/2
    ✔ Container python-playground  Removed                                                                                    10.5s 
    ✔ Network pydocker_default     Removed 
    ```

4. Start a new project with:
    In container terminal
    
    ```bash
    $ poetry new {project-name}
    ```

## How to Retain Installed Packages in the Container from the Last Development Session?

Needed to modify the `Dockerfile` and rebuild the Docker image. Ensure that the next time the container starts, it will download the project's packages according to the "package management config" (for `pip`, export `requirements.txt`; for `poetry`, use `pyproject.toml`).

Assuming that `matplotlib` is currently installed in the Docker container environment, here is the current project directory structure:

```
| - ...
| - Dockerfile
| - docker-compose.yml
| - workspace (which was created by `poetry new workspace`)
  | - pyproject.toml
```

### 1. Export Package Management

In the Poetry project, the `pyproject.toml` file will look like this:

```
...
[tool.poetry.dependencies]
python = "^3.10"
matplotlib = "^3.9.2"
```

### 2. Modify the `Dockerfile`

```dockerfile
...
WORKDIR /code/workspace

COPY workspace/pyproject.toml /code/workspace/pyproject.toml

RUN poetry install && rm -rf ${POETRY_CACHE_DIR}
```

### 3. Stop the Current Container, Rebuild the Image, and Start the Container

On your local machine:

```bash
$ docker compose down
$ docker compose up --build -d
```

After re-accessing the container, you can directly import `matplotlib` in the Python shell. As long as there are no changes to the packages, there’s no need to reinstall them when the Docker image is not rebuilt, making container shutdowns and restarts much faster.

**P.S.** The process is similar for pip, you just need to export the `requirements.txt` file:

```bash
$ pip list --format=freeze > requirements.txt
```

Dockerfile:

```dockerfile
WORKDIR /code/container-project-path

COPY {local-path/requirements.txt} /code/container-project-path/requirements.txt

RUN pip install -r requirements.txt
```