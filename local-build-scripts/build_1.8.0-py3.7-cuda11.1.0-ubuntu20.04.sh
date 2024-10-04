docker build -t liuyuweitarek/pytorch:1.8.0-py3.7-cuda11.1.0-ubuntu20.04 -f image-builder/docker/Ubuntu-Pip --build-arg PYTHON_VERSION=3.7 --build-arg UBUNTU_VERSION=20.04 --build-arg TORCH_PACKAGE_NAME=1.8.0+cu111 --build-arg TORCH_SOURCE_URL=https://download.pytorch.org/whl/cu111 --no-cache .
