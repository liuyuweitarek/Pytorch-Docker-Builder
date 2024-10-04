docker build -t liuyuweitarek/pytorch:2.2.1-py3.12-cuda12.1.0-ubuntu20.04 -f image-builder/docker/Ubuntu-Poetry --build-arg PYTHON_VERSION=3.12 --build-arg UBUNTU_VERSION=20.04 --build-arg PYPROJECT_FILE_DIR=image-builder/docker/default-workspace --build-arg DEFAULT_PYPROJECT_FILE=pytorch2.2.1-py3.12-cuda12.1.0-ubuntu20.04.toml --build-arg POETRY_VERSION=1.8.1 --no-cache .
