docker build -t liuyuweitarek/pytorch:1.13.0-py3.9-cuda11.6.2-ubuntu20.04 -f image-builder/docker/Ubuntu-Poetry --build-arg PYTHON_VERSION=3.9 --build-arg UBUNTU_VERSION=20.04 --build-arg PYPROJECT_FILE_DIR=image-builder/docker/default-workspace --build-arg DEFAULT_PYPROJECT_FILE=pytorch1.13.0-py3.9-cuda11.6.2-ubuntu20.04.toml --build-arg POETRY_VERSION=1.8.1 --no-cache .
