docker build -t liuyuweitarek/pytorch:1.10.1-py3.7-cuda11.3.1-ubuntu20.04 -f image-builder/docker/Ubuntu-Pip --build-arg PYTHON_VERSION=3.7 --build-arg UBUNTU_VERSION=20.04 --build-arg TORCH_PACKAGE_NAME=1.10.1+cu113 --build-arg TORCH_SOURCE_URL=https://download.pytorch.org/whl/cu113 --no-cache .
