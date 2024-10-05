PYPROJECT_TOML_DIR = "docker/default-workspace"
GITHUB_WORKFLOW_DIR = ".github/workflows"
LOCAL_BUILD_SCRIPTS_DIR = "local-build-scripts"
BADGES_DIR = "badges"

SOURCE_FILE = "config/source.json"
META_FILE = "config/meta.json"
ON_BUILDING_FILE = "config/on_building.json"
TARGET_FILE = "config/target.json"

TORCH_SOURCE_URL = "https://download.pytorch.org/whl/{CUDA_NAME}"

PYTHON_TAG = "https://img.shields.io/badge/Python-{PYTHON_VERSION}-blue?logo=python"
PYTORCH_TAG = "https://img.shields.io/badge/Pytorch-{TORCH_VERSION}-green?logo=pytorch"
CUDA_TAG = "https://img.shields.io/badge/Cuda-{CUDA_VERSION}-green?logo=nvidia"
UBUNTU_TAG = "https://img.shields.io/badge/Ubuntu-{UBUNTU_VERSION}-yellow?logo=ubuntu"

LOCAL_PYTHON_TAG = "[python{PYTHON_VERSION}]: https://github.com/liuyuweitarek/Pytorch-Docker-Builder/blob/main/image-builder/badges/python{PYTHON_VERSION}.svg"
LOCAL_PYTORCH_TAG = "[pytorch{TORCH_VERSION}]: https://github.com/liuyuweitarek/Pytorch-Docker-Builder/blob/main/image-builder/badges/pytorch{TORCH_VERSION}.svg"
LOCAL_CUDA_TAG = "[cuda{CUDA_VERSION}]: https://github.com/liuyuweitarek/Pytorch-Docker-Builder/blob/main/image-builder/badges/cuda{CUDA_VERSION}.svg"
LOCAL_UBUNTU_TAG = "[ubuntu{UBUNTU_VERSION}]: https://github.com/liuyuweitarek/Pytorch-Docker-Builder/blob/main/image-builder/badges/ubuntu{UBUNTU_VERSION}.svg"


class ImageState:
    PENDING = "Pending"
    NOT_BUILD_YET = "Not build yet"
    BUILD_SUCCESS = "Build Success"
    BUILD_FAILED = "Build Failed"