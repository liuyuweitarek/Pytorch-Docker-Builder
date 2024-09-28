pyproject_toml_template = """[tool.poetry]
name = "workspace"
version = "0.1.0"
description = "A playground for python project experiment."
authors = ["liuyuweitarek <liuyuwei.tarek@gmail.com>"]
license = "MIT"
readme = "README.md"

[tool.poetry.dependencies]
python="^{PYTHON_VERSION}"
torch={{version="{TORCH_PACKAGE_NAME}", source="torch"}}

[[tool.poetry.source]]
name = "PyPI"
priority = "primary"

[[tool.poetry.source]]
name = "torch"
url = "{TORCH_SOURCE_URL}"
priority = "supplemental"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
"""

local_poetry_build_script_template="""docker build \
-t {IMAGE_TAG} \
-f image-builder/docker/Ubuntu-Poetry \
--build-arg PYTHON_VERSION={PYTHON_VERSION} \
--build-arg UBUNTU_VERSION={UBUNTU_VERSION} \
--build-arg PYPROJECT_FILE_DIR={PYPROJECT_FILE_DIR} \
--build-arg DEFAULT_PYPROJECT_FILE={DEFAULT_PYPROJECT_FILE} \
--build-arg POETRY_VERSION=1.8.1 \
--no-cache .
"""

local_pip_build_script_template="""docker build \
-t {IMAGE_TAG} \
-f image-builder/docker/Ubuntu-Pip \
--build-arg PYTHON_VERSION={PYTHON_VERSION} \
--build-arg UBUNTU_VERSION={UBUNTU_VERSION} \
--build-arg TORCH_PACKAGE_NAME={TORCH_PACKAGE_NAME} \
--build-arg TORCH_SOURCE_URL={TORCH_SOURCE_URL} \
--no-cache .
"""

github_workflow_template="""name: Build Image({IMAGE_TAG})

env:
  PYTHON_VERSION: "{PYTHON_VERSION}"
  PACKAGE_MANAGEMENT: "{PACKAGE_MANAGEMENT}"
  POETRY_VERSION: "1.8.1"
  TORCH_PACKAGE_NAME: "{TORCH_PACKAGE_NAME}"
  TORCH_SOURCE_URL: "{TORCH_SOURCE_URL}"
  PYPROJECT_FILE_DIR: "{PYPROJECT_FILE_DIR}"
  DEFAULT_PYPROJECT_FILE: "{DEFAULT_PYPROJECT_FILE}"
  UBUNTU_VERSION: "{UBUNTU_VERSION}"

on:
  push:
    branches:
      - main
    paths:
      - {WORKFLOW_FILE}

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Login DockerHub
        run: docker login --username=${{{{ secrets.DOCKER_USERNAME }}}} --password=${{{{ secrets.DOCKER_PASSWORD }}}}

      - name: Build docker image
        run: |
          if [[ $PACKAGE_MANAGEMENT == 'poetry' ]]; then
              image-builder/docker/build-ubuntu-poetry.sh
          else
              image-builder/docker/build-ubuntu-pip.sh
          fi

      - name: Push docker image
        run: docker push {IMAGE_TAG}
"""
