ARG PYTHON_VERSION

FROM python:${PYTHON_VERSION}-slim as Base

ENV PROJECT_ROOT_DIR=$ROOT_DIR \
  DEBIAN_FRONTEND=noninteractive \ 
  # Python configuration:
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \ 
  PYTHONDONTWRITEBYTECODE=1 \
  # Poetry's configuration:
  POETRY_VERSION=1.8.1 \
  POETRY_HOME=/opt/poetry \
  POETRY_CACHE_DIR=/tmp/poetry_cache \
  POETRY_REQUESTS_TIMEOUT=3000 \
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_PREFER_ACTIVE_PYTHON=1 \
  POETRY_VIRTUALENVS_CREATE=0

RUN apt-get update \
    && apt install --no-install-recommends -y curl \
    && curl -sSL https://install.python-poetry.org | python - \
    && apt clean \
    && rm -rf /var/lib/apt/lists/*

ENV PATH="${POETRY_HOME}/bin:$PATH"

WORKDIR /code/workspace

COPY workspace/pyproject.toml /code/workspace/pyproject.toml

RUN poetry install && rm -rf ${POETRY_CACHE_DIR}