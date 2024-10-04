docker build -t liuyuweitarek/pytorch:2.4.1-py3.11-cuda12.0.0-ubuntu22.04 -f image-builder/docker/Ubuntu-Poetry --build-arg PYTHON_VERSION=3.11 --build-arg UBUNTU_VERSION=22.04 --build-arg PYPROJECT_FILE_DIR=image-builder/docker/default-workspace --build-arg DEFAULT_PYPROJECT_FILE=pytorch2.4.1-py3.11-cuda12.0.0-ubuntu22.04.toml --build-arg POETRY_VERSION=1.8.1 --no-cache .
