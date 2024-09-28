docker build \
-t ${IMAGE_TAG} \
-f image-builder/docker/Ubuntu-Poetry \
--build-arg PYTHON_VERSION=${PYTHON_VERSION} \
--build-arg UBUNTU_VERSION=${UBUNTU_VERSION} \
--build-arg PYPROJECT_FILE_DIR=${PYPROJECT_FILE_DIR} \
--build-arg DEFAULT_PYPROJECT_FILE=${DEFAULT_PYPROJECT_FILE} \
--build-arg POETRY_VERSION=1.8.1 \
--no-cache .