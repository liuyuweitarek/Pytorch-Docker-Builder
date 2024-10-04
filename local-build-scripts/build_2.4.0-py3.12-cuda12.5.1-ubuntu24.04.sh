docker build -t liuyuweitarek/pytorch:2.4.0-py3.12-cuda12.5.1-ubuntu24.04 -f image-builder/docker/Ubuntu-Poetry --build-arg PYTHON_VERSION=3.12 --build-arg UBUNTU_VERSION=24.04 --build-arg PYPROJECT_FILE_DIR=image-builder/docker/default-workspace --build-arg DEFAULT_PYPROJECT_FILE=pytorch2.4.0-py3.12-cuda12.5.1-ubuntu24.04.toml --build-arg POETRY_VERSION=1.8.1 --no-cache .
