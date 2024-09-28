docker build \
-t ${IMAGE_TAG} \
-f image-builder/docker/Ubuntu-Pip \
--build-arg PYTHON_VERSION=${PYTHON_VERSION} \
--build-arg UBUNTU_VERSION=${UBUNTU_VERSION} \
--build-arg TORCH_PACKAGE_NAME=${TORCH_PACKAGE_NAME} \ 
--build-arg TORCH_SOURCE_URL=${TORCH_SOURCE_URL} \
--no-cache .