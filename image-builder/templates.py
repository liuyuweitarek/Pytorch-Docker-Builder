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

[tool.poetry.group.test.dependencies]
pytest = "*"

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
  IMAGE_TAG: "{IMAGE_TAG}"
  PYTHON_VERSION: "{PYTHON_VERSION}"
  PACKAGE_MANAGEMENT: "{PACKAGE_MANAGEMENT}"
  POETRY_VERSION: "1.8.1"
  TORCH_VERSION: "{TORCH_VERSION}"
  TORCH_PACKAGE_NAME: "{TORCH_PACKAGE_NAME}"
  TORCH_SOURCE_URL: "{TORCH_SOURCE_URL}"
  PYPROJECT_FILE_DIR: "{PYPROJECT_FILE_DIR}"
  DEFAULT_PYPROJECT_FILE: "{DEFAULT_PYPROJECT_FILE}"
  CUDA_VERSION: "{CUDA_VERSION}"
  UBUNTU_VERSION: "{UBUNTU_VERSION}"

on:
  push:
    branches:
      - main
    paths:
      - {WORKFLOW_FILE}
  
  workflow_dispatch:

jobs:
  build-image:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Mock Login DockerHub
        run: |
          echo "${{{{ secrets.DOCKER_PASSWORD }}}}" | docker login -u "${{{{ secrets.DOCKER_USERNAME }}}}" --password-stdin

      - name: Build docker image
        run: |
          cd image-builder/docker
          if [[ $PACKAGE_MANAGEMENT == 'poetry' ]]; then
              bash build-ubuntu-poetry.sh
          else
              bash build-ubuntu-pip.sh
          fi
          cd ../..  

      # - name: Run Test Cases
      #   run: |
      #     docker run --rm -v $(pwd)/tests:/default-workspace/tests --name test-container --gpus all {IMAGE_TAG} bash -c "pytest tests"

      - name: Push Docker Image on Success && Record Success
        if: success()
        run: |
          docker push {IMAGE_TAG}
          echo "Record Success: {IMAGE_TAG}"
          docker rmi {IMAGE_TAG}
          docker run --rm -v $(pwd):/code --name update-readme-container liuyuweitarek/pytorch:update-readme bash -c "cd image-builder && python report.py  -t test-tag --torch-version {TORCH_VERSION} --python-version {PYTHON_VERSION} --cuda-version {CUDA_VERSION} --ubuntu-version {UBUNTU_VERSION} --build-result 'Build Success'"
      
      - name: Record Failure
        if: failure()
        run: |
          echo "Record Failure: {IMAGE_TAG}"
          docker run --rm -v $(pwd):/code --name update-readme-container liuyuweitarek/pytorch:update-readme bash -c "cd image-builder && python report.py  -t test-tag --torch-version {TORCH_VERSION} --python-version {PYTHON_VERSION} --cuda-version {CUDA_VERSION} --ubuntu-version {UBUNTU_VERSION} --build-result 'Build Failed'"
      
      - name: commit
        run: |
          git config --global user.email ${{{{ secrets.USER_EMAIL }}}}
          git config --global user.name ${{{{ secrets.USER_NAME }}}}
          git add README.md image-builder/config/source.json image-builder/config/badges.json
          git commit -m "Update README & source {IMAGE_TAG}" 
      
      - name: Push changes
        uses: liuyuweitarek/github-push-action@master
        with:
          github_token: ${{{{ secrets.GITHUB_TOKEN }}}}
  
"""

image_table_row_template = "| ![pytorch{TORCH_VERSION}] ![python{PYTHON_VERSION}] ![{PACKAGE_MANAGEMENT}] ![cuda{CUDA_VERSION}] ![ubuntu{UBUNTU_VERSION}] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/{TORCH_VERSION}-py{PYTHON_VERSION}-cuda{CUDA_VERSION}-ubuntu{UBUNTU_VERSION}?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/{TORCH_VERSION}-py{PYTHON_VERSION}-cuda{CUDA_VERSION}-ubuntu{UBUNTU_VERSION}` |"

raw_image_table_row_template = "| {TORCH_VERSION} | {PYTHON_VERSION} | {PACKAGE_MANAGEMENT} | {CUDA_VERSION} | {UBUNTU_VERSION} | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/{TORCH_VERSION}-py{PYTHON_VERSION}-cuda{CUDA_VERSION}-ubuntu{UBUNTU_VERSION}?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/{TORCH_VERSION}-py{PYTHON_VERSION}-cuda{CUDA_VERSION}-ubuntu{UBUNTU_VERSION}` |"
readme_template = """# Pytorch Docker Builder

[DockerHub]: https://hub.docker.com/r/liuyuweitarek/pytorch
[![Docker Stars](https://img.shields.io/docker/stars/liuyuweitarek/pytorch?logo=docker)][DockerHub]
[![Docker Pulls](https://img.shields.io/docker/pulls/liuyuweitarek/pytorch?logo=docker)][DockerHub]

Automate PyTorch Docker image builds with compatible Python, CUDA, and Poetry versions, including CI/CD for testing.

<!-- Package Management Tools -->
[Pip]: https://img.shields.io/badge/Pip-blue
[Poetry]: https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json


<!-- CUDA versions -->
{CUDA_TAGS}

<!-- Ubuntu versions -->
{UBUNTU_TAGS}

<!-- PyTorch versions -->
{PYTORCH_TAGS}

<!-- Python versions -->
{PYTHON_TAGS}

## Images

| Properties | Size | Commands |
| ---------- | ---- | -------- |
{IMAGE_TABLE}
"""
