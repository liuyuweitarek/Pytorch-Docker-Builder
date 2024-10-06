# Pytorch Docker Builder

[DockerHub]: https://hub.docker.com/r/liuyuweitarek/pytorch
[![Docker Stars](https://img.shields.io/docker/stars/liuyuweitarek/pytorch?logo=docker)][DockerHub]
[![Docker Pulls](https://img.shields.io/docker/pulls/liuyuweitarek/pytorch?logo=docker)][DockerHub]

Automate PyTorch Docker image builds with compatible Python, CUDA, and Poetry versions, including CI/CD for testing GPU import.

Find the image in [the table below](https://github.com/liuyuweitarek/Pytorch-Docker-Builder?tab=readme-ov-file#images) or search from the [DockerHub repository](https://hub.docker.com/r/liuyuweitarek/pytorch/tags) through `<>-py<>-cuda<>-ubuntu<>` format with corresponding version filled. 

> [!NOTE]
> **1. The images in the current project only cover Ubuntu version >= 20.04.**
>
> Lower versions of Ubuntu have more compatibility issues with PyTorch and CUDA, and require individual handling. You can refer to the guide for building your own image.
>
> **2. Poetry only supports Python >= 3.8**.
>
> Only images with Python >= 3.8 can use Poetry, while others use Pip.

## How do I know which image to use?

Install the valid version of cuda toolkit, refer to [these links](https://github.com/liuyuweitarek/Pytorch-Docker-Builder/edit/main/README.md#dependencies-references). Make sure that nvidia driver is [successfully installed](https://liuyuweitarek.github.io/python-poetry-wsl2-ubuntu-gpu-docker-template/getting_started/prerequisites/cuda-toolkit.html). Then, based on the `cuda version` you select, you can find the compatible `ubuntu version`, `python version` and `torch version` in [the config file](https://github.com/liuyuweitarek/Pytorch-Docker-Builder/blob/main/image-builder/config/compatible_versions.json). 

E.g. If you are using cuda `11.8.0`, in the [config file](https://github.com/liuyuweitarek/Pytorch-Docker-Builder/blob/main/image-builder/config/compatible_versions.json), you can find the compatible `python version`, `torch version` and `ubuntu version` as follows:

```json
{
    "11.8.0": {
        "package_name": "cu118",
        "python_available_torch": {
            "3.8": ["2.0.0", "2.0.1", "2.1.0", "2.1.1", "2.1.2", "2.2.0", "2.2.1", "2.2.2", "2.3.0", "2.3.1", "2.4.0", "2.4.1"],
            "3.9": ["2.0.0", "2.0.1", "2.1.0", "2.1.1", "2.1.2", "2.2.0", "2.2.1", "2.2.2", "2.3.0", "2.3.1", "2.4.0", "2.4.1"],
            "3.10": ["2.0.0", "2.0.1", "2.1.0", "2.1.1", "2.1.2", "2.2.0", "2.2.1", "2.2.2", "2.3.0", "2.3.1", "2.4.0", "2.4.1"],
            "3.11": ["2.0.0", "2.0.1", "2.1.0", "2.1.1", "2.1.2", "2.2.0", "2.2.1", "2.2.2", "2.3.0", "2.3.1", "2.4.0", "2.4.1"],
            "3.12": ["2.2.0", "2.2.1", "2.2.2", "2.3.0", "2.3.1", "2.4.0", "2.4.1"]
        },
        "ubuntu_avaiable": ["18.04", "20.04", "22.04"]
    }
}
```

Therefore, you can find which image to use or based the compatible versions build your own docker image.

## Prerequisites

For gpu usage, ensure your system meets the following requirements:

1. **Windows users need to enable WSL**  
   To run Docker with GPU support on Windows, you must enable Windows Subsystem for Linux (WSL).  
   Follow the instructions here: [Setting up WSL](https://liuyuweitarek.github.io/python-poetry-wsl2-ubuntu-gpu-docker-template/getting_started/prerequisites/windows-wsl.html).

2. **Install Docker**  
   - **Windows users:** Download and install [Docker Desktop](https://liuyuweitarek.github.io/python-poetry-wsl2-ubuntu-gpu-docker-template/getting_started/prerequisites/docker.html).  
   - **Linux users:** Install Docker Engine following the instructions [here](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository).

3. **Install CUDA Toolkit**  
   Ensure that your system has the CUDA Toolkit installed, which is necessary for GPU acceleration.  
   Refer to the guide: [Installing CUDA Toolkit](https://liuyuweitarek.github.io/python-poetry-wsl2-ubuntu-gpu-docker-template/getting_started/prerequisites/cuda-toolkit.html).

4. **Install NVIDIA Container Toolkit**  
   This is required to enable Docker containers to use the GPU.  
   Follow the instructions to install the NVIDIA Container Toolkit [here](https://liuyuweitarek.github.io/python-poetry-wsl2-ubuntu-gpu-docker-template/getting_started/prerequisites/nvidia-container-toolkit.html).

## How to run image directly and use for developing?

To directly use one of the prebuilt images for development, you can run the following command. This will mount your local directory to the container, so changes made within the container will be reflected in your file system.

```bash
docker run --gpus all -v /path/to/your/code:/workspace -w /workspace --rm -it liuyuweitarek/pytorch:<tag>
```

**Parameters:**

- `--gpus all`: Enables GPU support for the container.

- `-v /path/to/your/code:/workspace`: Mounts your local directory (/path/to/your/code) to the container's `/workspace` directory. 
  
  (P.S. Windows Powershell use `${PWD}`; Linux Bash use `$(pwd)`)

- `-w /workspace`: Sets the working directory to `/workspace` inside the container.

- `--rm`: Automatically removes the container when it exits.

- `-it`: Runs the container interactively.

**Example Output:**

- Executed command: `docker run --gpus all -v ${PWD}:/workspace -w /workspace --rm -it liuyuweitarek/pytorch:2.1.0-py3.10-cuda11.8.0-ubuntu20.04`
  
  (Linux user should replace `${PWD}` with `$(pwd)`)
  
  ```bash
  D:\github\docker-test> docker run --gpus all -v ${PWD}:/workspace -w /workspace --rm -it liuyuweitarek/pytorch:2.1.0-py3.10-cuda11.8.0-ubuntu20.04
  Unable to find image 'liuyuweitarek/pytorch:2.1.0-py3.10-cuda11.8.0-ubuntu20.04' locally
  2.1.0-py3.10-cuda11.8.0-ubuntu20.04: Pulling from liuyuweitarek/pytorch
  602d8ad51b81: Pull complete
  491247cf4999: Pull complete
  2a360d065640: Pull complete
  f5bd7a83aedf: Pull complete
  Digest: sha256:e95807387b8aae98fa2be170a61422e2ed0418af035439510954c267e21a6b6f
  root@508a87161783:/workspace#
  ```

**Check PyTorch Import && GPU Usage:**

  ```bash
  root@91e7471b0705:/workspace# python
  Python 3.10.15 (main, Sep  7 2024, 18:35:33) [GCC 9.4.0] on linux
  Type "help", "copyright", "credits" or "license" for more information.
  >>> import torch
  >>> torch.cuda.is_available()
  True
  ``` 

**Check Poetry Dependencies:**
  
Current folder file structure:
    
- Local machine: `D:\github\docker-test`
  
  (No files)

- Container: `/workspace`  
  
  (No files)

Try to start a new poetry project, sync pyproject.toml and add new package:
  
  ```bash
  # Poetry Used
  root@91e7471b0705:/workspace# which poetry
  /opt/poetry/bin/poetry

  # Start a new poetry project. More details for poetry usage: https://python-poetry.org/docs/basic-usage/
  root@91e7471b0705:/workspace# poetry new my-project
  Created package my_project in my-project
  .
    |-my-project
    | |-my_project
    | | |-__init__.py
    | |-pyproject.toml
    | |-README.md
    | |-tests
    | | |-__init__.py
  
  # Sync pyproject.toml
  root@91e7471b0705:/workspace# cp /default-workspace/pyproject.toml /workspace/my-project/pyproject.toml
  
  # Add new package
  root@91e7471b0705:/workspace# python
  Python 3.10.15 (main, Sep  7 2024, 18:37:45) [GCC 9.4.0] on linux
  Type "help", "copyright", "credits" or "license" for more information.
  >>> import matplotlib
  Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
  ModuleNotFoundError: No module named 'matplotlib'
  >>> exit()

  root@91e7471b0705:/workspace# cd my-project/
  root@91e7471b0705:/workspace/my-project# poetry add matplotlib
  Skipping virtualenv creation, as specified in config file.
  Using version ^3.9.2 for matplotlib

  Updating dependencies
  Resolving dependencies... (6.2s)

  Package operations: 8 installs, 1 update, 0 removals

    - Updating six (1.14.0 /usr/lib/python3/dist-packages -> 1.16.0)
    - Installing contourpy (1.3.0)
    - Installing cycler (0.12.1)
    - Installing fonttools (4.54.1)
    - Installing kiwisolver (1.4.7)
    - Installing pillow (10.4.0)
    - Installing pyparsing (3.1.4)
    - Installing python-dateutil (2.9.0.post0)
    - Installing matplotlib (3.9.2)

  Writing lock file
  root@91e7471b0705:/workspace/my-project# python
  Python 3.10.15 (main, Sep  7 2024, 18:35:33) [GCC 9.4.0] on linux
  Type "help", "copyright", "credits" or "license" for more information.
  >>> import matplotlib
  >>>
  ```

Current folder file structure:
    
- Local machine: `D:\github\docker-test`
 
  ```
  .
    |-my-project
    | |-my_project
    | | |-__init__.py
    | |-poetry.lock
    | |-pyproject.toml
    | |-README.md
    | |-tests
    | | |-__init__.py
  ```

- Container: `/workspace`  
 
  ```
  .
    |-my-project
    | |-my_project
    | | |-__init__.py
    | |-poetry.lock
    | |-pyproject.toml
    | |-README.md
    | |-tests
    | | |-__init__.py
  ```

**Stop the container && Restart the container:**

- Stop the container: `Ctrl+D`

  Due to `--rm` option, the container will be removed after exit; however, the image still retains, so don't need to take time for pulling down image again.

- Restart the container
  
  Under `D:\github\docker-test`, run docker command again. However, we lost the package just installed.  

  ```bash
  PS D:\github\docker-test> docker run --gpus all -v ${PWD}:/workspace -w /workspace --rm -it liuyuweitarek/pytorch:2.1.0-py3.10-cuda11.8.0-ubuntu20.04
  root@65078665a0e9:/workspace# python
  Python 3.10.15 (main, Sep  7 2024, 18:35:33) [GCC 9.4.0] on linux
  Type "help", "copyright", "credits" or "license" for more information.
  >>> import matplotlib
  Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
  ModuleNotFoundError: No module named 'matplotlib'
  >>>
  ```

  **Reinstall the package:**
  
  ```bash
  root@65078665a0e9:/workspace/my-project# poetry install
  ```
  
  If you want to pretain the package just installed, and use directly without reinstalling, you need to build a new image. Please watch the next section.

## Build your own image 

Add `Dockerfile` to your project folder. Here I use `D:\github\docker-test`, folder structure be like:
 
  ```
  .
    |-my-project
    | |-my_project
    | | |-__init__.py
    | |-poetry.lock
    | |-pyproject.toml
    | |-README.md
    | |-tests
    | | |-__init__.py
    | |-Dockerfile ---> Here
  ```

**`Dockerfile`**

```dockerfile
FROM liuyuweitarek/pytorch:2.1.0-py3.10-cuda11.8.0-ubuntu20.04

WORKDIR /workspace/my-project

## Note: For solved matplotlib install error
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python
RUN python -m pip  install --upgrade pip

COPY my-project/pyproject.toml my-project/poetry.lock ./

RUN poetry install 
```

**Under Root Folder(`D:\github\docker-test`) build your image**

```bash
$ docker build -t my-project-image -f my-project/Dockerfile .
```

**RUN your image**

```bash   
$ docker run --gpus all -v ${PWD}:/workspace -w /workspace --rm -it my-project-image

root@6057cc148ae7:/workspace#
root@6057cc148ae7:/workspace# python
Python 3.10.15 (main, Sep  7 2024, 18:35:33) [GCC 9.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import matplotlib
>>> import torch
>>> torch.cuda.is_available()
True 
```

Done!

<!-- Package Management Tools -->
[Pip]: https://img.shields.io/badge/Pip-blue
[Poetry]: https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json

<!-- CUDA versions -->
[cuda12.6.1]: https://github.com/liuyuweitarek/Pytorch-Docker-Builder/blob/main/image-builder/badges/cuda12.6.1.svg
[cuda12.5.1]: https://github.com/liuyuweitarek/Pytorch-Docker-Builder/blob/main/image-builder/badges/cuda12.5.1.svg
[cuda12.3.2]: https://github.com/liuyuweitarek/Pytorch-Docker-Builder/blob/main/image-builder/badges/cuda12.3.2.svg
[cuda12.2.2]: https://github.com/liuyuweitarek/Pytorch-Docker-Builder/blob/main/image-builder/badges/cuda12.2.2.svg
[cuda12.1.0]: https://github.com/liuyuweitarek/Pytorch-Docker-Builder/blob/main/image-builder/badges/cuda12.1.0.svg
[cuda12.0.0]: https://github.com/liuyuweitarek/Pytorch-Docker-Builder/blob/main/image-builder/badges/cuda12.0.0.svg
[cuda11.8.0]: https://github.com/liuyuweitarek/Pytorch-Docker-Builder/blob/main/image-builder/badges/cuda11.8.0.svg
[cuda11.7.1]: https://github.com/liuyuweitarek/Pytorch-Docker-Builder/blob/main/image-builder/badges/cuda11.7.1.svg
[cuda11.6.2]: https://github.com/liuyuweitarek/Pytorch-Docker-Builder/blob/main/image-builder/badges/cuda11.6.2.svg
[cuda11.5.2]: https://github.com/liuyuweitarek/Pytorch-Docker-Builder/blob/main/image-builder/badges/cuda11.5.2.svg
[cuda11.3.1]: https://github.com/liuyuweitarek/Pytorch-Docker-Builder/blob/main/image-builder/badges/cuda11.3.1.svg
[cuda11.1.1]: https://github.com/liuyuweitarek/Pytorch-Docker-Builder/blob/main/image-builder/badges/cuda11.1.1.svg
[cuda11.1.0]: https://github.com/liuyuweitarek/Pytorch-Docker-Builder/blob/main/image-builder/badges/cuda11.1.0.svg
[cuda11.0]: https://github.com/liuyuweitarek/Pytorch-Docker-Builder/blob/main/image-builder/badges/cuda11.0.svg

<!-- Ubuntu versions -->
[ubuntu24.04]: https://github.com/liuyuweitarek/Pytorch-Docker-Builder/blob/main/image-builder/badges/ubuntu24.04.svg
[ubuntu22.04]: https://github.com/liuyuweitarek/Pytorch-Docker-Builder/blob/main/image-builder/badges/ubuntu22.04.svg
[ubuntu20.04]: https://github.com/liuyuweitarek/Pytorch-Docker-Builder/blob/main/image-builder/badges/ubuntu20.04.svg

<!-- PyTorch versions -->
[pytorch2.4.1]: https://github.com/liuyuweitarek/Pytorch-Docker-Builder/blob/main/image-builder/badges/pytorch2.4.1.svg
[pytorch2.4.0]: https://github.com/liuyuweitarek/Pytorch-Docker-Builder/blob/main/image-builder/badges/pytorch2.4.0.svg
[pytorch2.2.0]: https://github.com/liuyuweitarek/Pytorch-Docker-Builder/blob/main/image-builder/badges/pytorch2.2.0.svg
[pytorch2.1.2]: https://github.com/liuyuweitarek/Pytorch-Docker-Builder/blob/main/image-builder/badges/pytorch2.1.2.svg
[pytorch2.1.1]: https://github.com/liuyuweitarek/Pytorch-Docker-Builder/blob/main/image-builder/badges/pytorch2.1.1.svg
[pytorch2.1.0]: https://github.com/liuyuweitarek/Pytorch-Docker-Builder/blob/main/image-builder/badges/pytorch2.1.0.svg
[pytorch2.0.1]: https://github.com/liuyuweitarek/Pytorch-Docker-Builder/blob/main/image-builder/badges/pytorch2.0.1.svg
[pytorch2.0.0]: https://github.com/liuyuweitarek/Pytorch-Docker-Builder/blob/main/image-builder/badges/pytorch2.0.0.svg
[pytorch1.9.1]: https://github.com/liuyuweitarek/Pytorch-Docker-Builder/blob/main/image-builder/badges/pytorch1.9.1.svg
[pytorch1.9.0]: https://github.com/liuyuweitarek/Pytorch-Docker-Builder/blob/main/image-builder/badges/pytorch1.9.0.svg
[pytorch1.8.1]: https://github.com/liuyuweitarek/Pytorch-Docker-Builder/blob/main/image-builder/badges/pytorch1.8.1.svg
[pytorch1.8.0]: https://github.com/liuyuweitarek/Pytorch-Docker-Builder/blob/main/image-builder/badges/pytorch1.8.0.svg
[pytorch1.7.1]: https://github.com/liuyuweitarek/Pytorch-Docker-Builder/blob/main/image-builder/badges/pytorch1.7.1.svg
[pytorch1.7.0]: https://github.com/liuyuweitarek/Pytorch-Docker-Builder/blob/main/image-builder/badges/pytorch1.7.0.svg
[pytorch1.13.1]: https://github.com/liuyuweitarek/Pytorch-Docker-Builder/blob/main/image-builder/badges/pytorch1.13.1.svg
[pytorch1.13.0]: https://github.com/liuyuweitarek/Pytorch-Docker-Builder/blob/main/image-builder/badges/pytorch1.13.0.svg
[pytorch1.12.1]: https://github.com/liuyuweitarek/Pytorch-Docker-Builder/blob/main/image-builder/badges/pytorch1.12.1.svg
[pytorch1.12.0]: https://github.com/liuyuweitarek/Pytorch-Docker-Builder/blob/main/image-builder/badges/pytorch1.12.0.svg
[pytorch1.11.0]: https://github.com/liuyuweitarek/Pytorch-Docker-Builder/blob/main/image-builder/badges/pytorch1.11.0.svg
[pytorch1.10.2]: https://github.com/liuyuweitarek/Pytorch-Docker-Builder/blob/main/image-builder/badges/pytorch1.10.2.svg
[pytorch1.10.1]: https://github.com/liuyuweitarek/Pytorch-Docker-Builder/blob/main/image-builder/badges/pytorch1.10.1.svg
[pytorch1.10.0]: https://github.com/liuyuweitarek/Pytorch-Docker-Builder/blob/main/image-builder/badges/pytorch1.10.0.svg

<!-- Python versions -->
[python3.11]: https://github.com/liuyuweitarek/Pytorch-Docker-Builder/blob/main/image-builder/badges/python3.11.svg
[python3.10]: https://github.com/liuyuweitarek/Pytorch-Docker-Builder/blob/main/image-builder/badges/python3.10.svg
[python3.9]: https://github.com/liuyuweitarek/Pytorch-Docker-Builder/blob/main/image-builder/badges/python3.9.svg
[python3.8]: https://github.com/liuyuweitarek/Pytorch-Docker-Builder/blob/main/image-builder/badges/python3.8.svg
[python3.7]: https://github.com/liuyuweitarek/Pytorch-Docker-Builder/blob/main/image-builder/badges/python3.7.svg
[python3.6]: https://github.com/liuyuweitarek/Pytorch-Docker-Builder/blob/main/image-builder/badges/python3.6.svg

## Images

| Properties | Size | Commands |
| ---------- | ---- | -------- |
| ![pytorch2.4.1] ![python3.9] ![Poetry] ![cuda12.5.1] ![ubuntu24.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.4.1-py3.9-cuda12.5.1-ubuntu24.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.4.1-py3.9-cuda12.5.1-ubuntu24.04` |
| ![pytorch2.4.1] ![python3.9] ![Poetry] ![cuda12.6.1] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.4.1-py3.9-cuda12.6.1-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.4.1-py3.9-cuda12.6.1-ubuntu20.04` |
| ![pytorch2.4.1] ![python3.9] ![Poetry] ![cuda12.6.1] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.4.1-py3.9-cuda12.6.1-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.4.1-py3.9-cuda12.6.1-ubuntu22.04` |
| ![pytorch2.4.1] ![python3.9] ![Poetry] ![cuda12.6.1] ![ubuntu24.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.4.1-py3.9-cuda12.6.1-ubuntu24.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.4.1-py3.9-cuda12.6.1-ubuntu24.04` |
| ![pytorch2.4.0] ![python3.11] ![Poetry] ![cuda12.5.1] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.4.0-py3.11-cuda12.5.1-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.4.0-py3.11-cuda12.5.1-ubuntu22.04` |
| ![pytorch2.2.0] ![python3.10] ![Poetry] ![cuda11.8.0] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.2.0-py3.10-cuda11.8.0-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.2.0-py3.10-cuda11.8.0-ubuntu22.04` |
| ![pytorch2.2.0] ![python3.10] ![Poetry] ![cuda12.0.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.2.0-py3.10-cuda12.0.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.2.0-py3.10-cuda12.0.0-ubuntu20.04` |
| ![pytorch2.2.0] ![python3.10] ![Poetry] ![cuda11.8.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.2.0-py3.10-cuda11.8.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.2.0-py3.10-cuda11.8.0-ubuntu20.04` |
| ![pytorch2.2.0] ![python3.10] ![Poetry] ![cuda12.1.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.2.0-py3.10-cuda12.1.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.2.0-py3.10-cuda12.1.0-ubuntu20.04` |
| ![pytorch2.2.0] ![python3.10] ![Poetry] ![cuda12.0.0] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.2.0-py3.10-cuda12.0.0-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.2.0-py3.10-cuda12.0.0-ubuntu22.04` |
| ![pytorch2.2.0] ![python3.10] ![Poetry] ![cuda12.2.2] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.2.0-py3.10-cuda12.2.2-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.2.0-py3.10-cuda12.2.2-ubuntu20.04` |
| ![pytorch2.2.0] ![python3.10] ![Poetry] ![cuda12.1.0] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.2.0-py3.10-cuda12.1.0-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.2.0-py3.10-cuda12.1.0-ubuntu22.04` |
| ![pytorch2.1.2] ![python3.10] ![Poetry] ![cuda12.0.0] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.2-py3.10-cuda12.0.0-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.2-py3.10-cuda12.0.0-ubuntu22.04` |
| ![pytorch2.1.2] ![python3.9] ![Poetry] ![cuda11.8.0] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.2-py3.9-cuda11.8.0-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.2-py3.9-cuda11.8.0-ubuntu22.04` |
| ![pytorch2.1.2] ![python3.9] ![Poetry] ![cuda12.3.2] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.2-py3.9-cuda12.3.2-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.2-py3.9-cuda12.3.2-ubuntu22.04` |
| ![pytorch2.1.2] ![python3.10] ![Poetry] ![cuda12.2.2] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.2-py3.10-cuda12.2.2-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.2-py3.10-cuda12.2.2-ubuntu20.04` |
| ![pytorch2.1.2] ![python3.10] ![Poetry] ![cuda12.1.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.2-py3.10-cuda12.1.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.2-py3.10-cuda12.1.0-ubuntu20.04` |
| ![pytorch2.1.2] ![python3.9] ![Poetry] ![cuda11.8.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.2-py3.9-cuda11.8.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.2-py3.9-cuda11.8.0-ubuntu20.04` |
| ![pytorch2.1.2] ![python3.10] ![Poetry] ![cuda12.3.2] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.2-py3.10-cuda12.3.2-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.2-py3.10-cuda12.3.2-ubuntu20.04` |
| ![pytorch2.1.2] ![python3.10] ![Poetry] ![cuda11.8.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.2-py3.10-cuda11.8.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.2-py3.10-cuda11.8.0-ubuntu20.04` |
| ![pytorch2.1.2] ![python3.9] ![Poetry] ![cuda12.2.2] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.2-py3.9-cuda12.2.2-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.2-py3.9-cuda12.2.2-ubuntu22.04` |
| ![pytorch2.1.2] ![python3.8] ![Poetry] ![cuda12.3.2] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.2-py3.8-cuda12.3.2-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.2-py3.8-cuda12.3.2-ubuntu22.04` |
| ![pytorch2.1.2] ![python3.8] ![Poetry] ![cuda12.3.2] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.2-py3.8-cuda12.3.2-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.2-py3.8-cuda12.3.2-ubuntu20.04` |
| ![pytorch2.1.2] ![python3.11] ![Poetry] ![cuda12.0.0] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.2-py3.11-cuda12.0.0-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.2-py3.11-cuda12.0.0-ubuntu22.04` |
| ![pytorch2.1.2] ![python3.11] ![Poetry] ![cuda12.3.2] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.2-py3.11-cuda12.3.2-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.2-py3.11-cuda12.3.2-ubuntu20.04` |
| ![pytorch2.1.2] ![python3.11] ![Poetry] ![cuda12.3.2] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.2-py3.11-cuda12.3.2-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.2-py3.11-cuda12.3.2-ubuntu22.04` |
| ![pytorch2.1.2] ![python3.11] ![Poetry] ![cuda12.2.2] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.2-py3.11-cuda12.2.2-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.2-py3.11-cuda12.2.2-ubuntu20.04` |
| ![pytorch2.1.2] ![python3.8] ![Poetry] ![cuda12.0.0] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.2-py3.8-cuda12.0.0-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.2-py3.8-cuda12.0.0-ubuntu22.04` |
| ![pytorch2.1.2] ![python3.8] ![Poetry] ![cuda12.2.2] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.2-py3.8-cuda12.2.2-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.2-py3.8-cuda12.2.2-ubuntu22.04` |
| ![pytorch2.1.2] ![python3.9] ![Poetry] ![cuda12.1.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.2-py3.9-cuda12.1.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.2-py3.9-cuda12.1.0-ubuntu20.04` |
| ![pytorch2.1.2] ![python3.8] ![Poetry] ![cuda12.2.2] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.2-py3.8-cuda12.2.2-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.2-py3.8-cuda12.2.2-ubuntu20.04` |
| ![pytorch2.1.2] ![python3.11] ![Poetry] ![cuda12.1.0] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.2-py3.11-cuda12.1.0-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.2-py3.11-cuda12.1.0-ubuntu22.04` |
| ![pytorch2.1.2] ![python3.9] ![Poetry] ![cuda12.0.0] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.2-py3.9-cuda12.0.0-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.2-py3.9-cuda12.0.0-ubuntu22.04` |
| ![pytorch2.1.2] ![python3.10] ![Poetry] ![cuda12.0.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.2-py3.10-cuda12.0.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.2-py3.10-cuda12.0.0-ubuntu20.04` |
| ![pytorch2.1.2] ![python3.11] ![Poetry] ![cuda12.2.2] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.2-py3.11-cuda12.2.2-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.2-py3.11-cuda12.2.2-ubuntu22.04` |
| ![pytorch2.1.2] ![python3.8] ![Poetry] ![cuda11.8.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.2-py3.8-cuda11.8.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.2-py3.8-cuda11.8.0-ubuntu20.04` |
| ![pytorch2.1.2] ![python3.9] ![Poetry] ![cuda12.1.0] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.2-py3.9-cuda12.1.0-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.2-py3.9-cuda12.1.0-ubuntu22.04` |
| ![pytorch2.1.2] ![python3.9] ![Poetry] ![cuda12.2.2] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.2-py3.9-cuda12.2.2-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.2-py3.9-cuda12.2.2-ubuntu20.04` |
| ![pytorch2.1.2] ![python3.11] ![Poetry] ![cuda12.1.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.2-py3.11-cuda12.1.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.2-py3.11-cuda12.1.0-ubuntu20.04` |
| ![pytorch2.1.2] ![python3.9] ![Poetry] ![cuda12.3.2] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.2-py3.9-cuda12.3.2-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.2-py3.9-cuda12.3.2-ubuntu20.04` |
| ![pytorch2.1.2] ![python3.8] ![Poetry] ![cuda12.1.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.2-py3.8-cuda12.1.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.2-py3.8-cuda12.1.0-ubuntu20.04` |
| ![pytorch2.1.2] ![python3.8] ![Poetry] ![cuda12.1.0] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.2-py3.8-cuda12.1.0-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.2-py3.8-cuda12.1.0-ubuntu22.04` |
| ![pytorch2.1.2] ![python3.11] ![Poetry] ![cuda11.8.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.2-py3.11-cuda11.8.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.2-py3.11-cuda11.8.0-ubuntu20.04` |
| ![pytorch2.1.2] ![python3.10] ![Poetry] ![cuda12.2.2] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.2-py3.10-cuda12.2.2-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.2-py3.10-cuda12.2.2-ubuntu22.04` |
| ![pytorch2.1.2] ![python3.11] ![Poetry] ![cuda12.0.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.2-py3.11-cuda12.0.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.2-py3.11-cuda12.0.0-ubuntu20.04` |
| ![pytorch2.1.2] ![python3.10] ![Poetry] ![cuda12.3.2] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.2-py3.10-cuda12.3.2-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.2-py3.10-cuda12.3.2-ubuntu22.04` |
| ![pytorch2.1.2] ![python3.8] ![Poetry] ![cuda11.8.0] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.2-py3.8-cuda11.8.0-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.2-py3.8-cuda11.8.0-ubuntu22.04` |
| ![pytorch2.1.2] ![python3.8] ![Poetry] ![cuda12.0.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.2-py3.8-cuda12.0.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.2-py3.8-cuda12.0.0-ubuntu20.04` |
| ![pytorch2.1.2] ![python3.11] ![Poetry] ![cuda11.8.0] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.2-py3.11-cuda11.8.0-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.2-py3.11-cuda11.8.0-ubuntu22.04` |
| ![pytorch2.1.2] ![python3.10] ![Poetry] ![cuda12.1.0] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.2-py3.10-cuda12.1.0-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.2-py3.10-cuda12.1.0-ubuntu22.04` |
| ![pytorch2.1.2] ![python3.10] ![Poetry] ![cuda11.8.0] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.2-py3.10-cuda11.8.0-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.2-py3.10-cuda11.8.0-ubuntu22.04` |
| ![pytorch2.1.2] ![python3.9] ![Poetry] ![cuda12.0.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.2-py3.9-cuda12.0.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.2-py3.9-cuda12.0.0-ubuntu20.04` |
| ![pytorch2.1.1] ![python3.11] ![Poetry] ![cuda12.1.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.1-py3.11-cuda12.1.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.1-py3.11-cuda12.1.0-ubuntu20.04` |
| ![pytorch2.1.1] ![python3.10] ![Poetry] ![cuda12.0.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.1-py3.10-cuda12.0.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.1-py3.10-cuda12.0.0-ubuntu20.04` |
| ![pytorch2.1.1] ![python3.11] ![Poetry] ![cuda12.2.2] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.1-py3.11-cuda12.2.2-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.1-py3.11-cuda12.2.2-ubuntu22.04` |
| ![pytorch2.1.1] ![python3.8] ![Poetry] ![cuda12.0.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.1-py3.8-cuda12.0.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.1-py3.8-cuda12.0.0-ubuntu20.04` |
| ![pytorch2.1.1] ![python3.9] ![Poetry] ![cuda12.3.2] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.1-py3.9-cuda12.3.2-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.1-py3.9-cuda12.3.2-ubuntu20.04` |
| ![pytorch2.1.1] ![python3.10] ![Poetry] ![cuda12.0.0] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.1-py3.10-cuda12.0.0-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.1-py3.10-cuda12.0.0-ubuntu22.04` |
| ![pytorch2.1.1] ![python3.9] ![Poetry] ![cuda11.8.0] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.1-py3.9-cuda11.8.0-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.1-py3.9-cuda11.8.0-ubuntu22.04` |
| ![pytorch2.1.1] ![python3.10] ![Poetry] ![cuda12.3.2] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.1-py3.10-cuda12.3.2-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.1-py3.10-cuda12.3.2-ubuntu22.04` |
| ![pytorch2.1.1] ![python3.11] ![Poetry] ![cuda12.3.2] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.1-py3.11-cuda12.3.2-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.1-py3.11-cuda12.3.2-ubuntu22.04` |
| ![pytorch2.1.1] ![python3.10] ![Poetry] ![cuda12.2.2] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.1-py3.10-cuda12.2.2-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.1-py3.10-cuda12.2.2-ubuntu22.04` |
| ![pytorch2.1.1] ![python3.11] ![Poetry] ![cuda11.8.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.1-py3.11-cuda11.8.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.1-py3.11-cuda11.8.0-ubuntu20.04` |
| ![pytorch2.1.1] ![python3.9] ![Poetry] ![cuda12.0.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.1-py3.9-cuda12.0.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.1-py3.9-cuda12.0.0-ubuntu20.04` |
| ![pytorch2.1.1] ![python3.11] ![Poetry] ![cuda12.0.0] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.1-py3.11-cuda12.0.0-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.1-py3.11-cuda12.0.0-ubuntu22.04` |
| ![pytorch2.1.1] ![python3.11] ![Poetry] ![cuda12.2.2] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.1-py3.11-cuda12.2.2-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.1-py3.11-cuda12.2.2-ubuntu20.04` |
| ![pytorch2.1.1] ![python3.9] ![Poetry] ![cuda12.2.2] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.1-py3.9-cuda12.2.2-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.1-py3.9-cuda12.2.2-ubuntu20.04` |
| ![pytorch2.1.1] ![python3.11] ![Poetry] ![cuda12.0.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.1-py3.11-cuda12.0.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.1-py3.11-cuda12.0.0-ubuntu20.04` |
| ![pytorch2.1.1] ![python3.11] ![Poetry] ![cuda12.3.2] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.1-py3.11-cuda12.3.2-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.1-py3.11-cuda12.3.2-ubuntu20.04` |
| ![pytorch2.1.1] ![python3.11] ![Poetry] ![cuda11.8.0] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.1-py3.11-cuda11.8.0-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.1-py3.11-cuda11.8.0-ubuntu22.04` |
| ![pytorch2.1.1] ![python3.10] ![Poetry] ![cuda12.1.0] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.1-py3.10-cuda12.1.0-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.1-py3.10-cuda12.1.0-ubuntu22.04` |
| ![pytorch2.1.1] ![python3.8] ![Poetry] ![cuda11.8.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.1-py3.8-cuda11.8.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.1-py3.8-cuda11.8.0-ubuntu20.04` |
| ![pytorch2.1.1] ![python3.9] ![Poetry] ![cuda11.8.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.1-py3.9-cuda11.8.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.1-py3.9-cuda11.8.0-ubuntu20.04` |
| ![pytorch2.1.1] ![python3.9] ![Poetry] ![cuda12.2.2] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.1-py3.9-cuda12.2.2-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.1-py3.9-cuda12.2.2-ubuntu22.04` |
| ![pytorch2.1.1] ![python3.9] ![Poetry] ![cuda12.3.2] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.1-py3.9-cuda12.3.2-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.1-py3.9-cuda12.3.2-ubuntu22.04` |
| ![pytorch2.1.1] ![python3.9] ![Poetry] ![cuda12.1.0] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.1-py3.9-cuda12.1.0-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.1-py3.9-cuda12.1.0-ubuntu22.04` |
| ![pytorch2.1.1] ![python3.8] ![Poetry] ![cuda12.3.2] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.1-py3.8-cuda12.3.2-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.1-py3.8-cuda12.3.2-ubuntu20.04` |
| ![pytorch2.1.1] ![python3.9] ![Poetry] ![cuda12.1.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.1-py3.9-cuda12.1.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.1-py3.9-cuda12.1.0-ubuntu20.04` |
| ![pytorch2.1.1] ![python3.8] ![Poetry] ![cuda12.0.0] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.1-py3.8-cuda12.0.0-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.1-py3.8-cuda12.0.0-ubuntu22.04` |
| ![pytorch2.1.1] ![python3.8] ![Poetry] ![cuda12.2.2] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.1-py3.8-cuda12.2.2-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.1-py3.8-cuda12.2.2-ubuntu20.04` |
| ![pytorch2.1.1] ![python3.10] ![Poetry] ![cuda12.1.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.1-py3.10-cuda12.1.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.1-py3.10-cuda12.1.0-ubuntu20.04` |
| ![pytorch2.1.1] ![python3.10] ![Poetry] ![cuda12.3.2] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.1-py3.10-cuda12.3.2-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.1-py3.10-cuda12.3.2-ubuntu20.04` |
| ![pytorch2.1.1] ![python3.10] ![Poetry] ![cuda11.8.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.1-py3.10-cuda11.8.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.1-py3.10-cuda11.8.0-ubuntu20.04` |
| ![pytorch2.1.1] ![python3.10] ![Poetry] ![cuda11.8.0] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.1-py3.10-cuda11.8.0-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.1-py3.10-cuda11.8.0-ubuntu22.04` |
| ![pytorch2.1.1] ![python3.11] ![Poetry] ![cuda12.1.0] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.1-py3.11-cuda12.1.0-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.1-py3.11-cuda12.1.0-ubuntu22.04` |
| ![pytorch2.1.1] ![python3.8] ![Poetry] ![cuda11.8.0] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.1-py3.8-cuda11.8.0-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.1-py3.8-cuda11.8.0-ubuntu22.04` |
| ![pytorch2.1.1] ![python3.9] ![Poetry] ![cuda12.0.0] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.1-py3.9-cuda12.0.0-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.1-py3.9-cuda12.0.0-ubuntu22.04` |
| ![pytorch2.1.1] ![python3.8] ![Poetry] ![cuda12.3.2] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.1-py3.8-cuda12.3.2-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.1-py3.8-cuda12.3.2-ubuntu22.04` |
| ![pytorch2.1.1] ![python3.8] ![Poetry] ![cuda12.2.2] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.1-py3.8-cuda12.2.2-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.1-py3.8-cuda12.2.2-ubuntu22.04` |
| ![pytorch2.1.1] ![python3.8] ![Poetry] ![cuda12.1.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.1-py3.8-cuda12.1.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.1-py3.8-cuda12.1.0-ubuntu20.04` |
| ![pytorch2.1.1] ![python3.10] ![Poetry] ![cuda12.2.2] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.1-py3.10-cuda12.2.2-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.1-py3.10-cuda12.2.2-ubuntu20.04` |
| ![pytorch2.1.1] ![python3.8] ![Poetry] ![cuda12.1.0] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.1-py3.8-cuda12.1.0-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.1-py3.8-cuda12.1.0-ubuntu22.04` |
| ![pytorch2.1.0] ![python3.11] ![Poetry] ![cuda12.1.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.0-py3.11-cuda12.1.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.0-py3.11-cuda12.1.0-ubuntu20.04` |
| ![pytorch2.1.0] ![python3.9] ![Poetry] ![cuda12.1.0] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.0-py3.9-cuda12.1.0-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.0-py3.9-cuda12.1.0-ubuntu22.04` |
| ![pytorch2.1.0] ![python3.11] ![Poetry] ![cuda12.0.0] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.0-py3.11-cuda12.0.0-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.0-py3.11-cuda12.0.0-ubuntu22.04` |
| ![pytorch2.1.0] ![python3.8] ![Poetry] ![cuda11.8.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.0-py3.8-cuda11.8.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.0-py3.8-cuda11.8.0-ubuntu20.04` |
| ![pytorch2.1.0] ![python3.11] ![Poetry] ![cuda12.2.2] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.0-py3.11-cuda12.2.2-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.0-py3.11-cuda12.2.2-ubuntu22.04` |
| ![pytorch2.1.0] ![python3.8] ![Poetry] ![cuda12.0.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.0-py3.8-cuda12.0.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.0-py3.8-cuda12.0.0-ubuntu20.04` |
| ![pytorch2.1.0] ![python3.8] ![Poetry] ![cuda12.1.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.0-py3.8-cuda12.1.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.0-py3.8-cuda12.1.0-ubuntu20.04` |
| ![pytorch2.1.0] ![python3.11] ![Poetry] ![cuda12.0.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.0-py3.11-cuda12.0.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.0-py3.11-cuda12.0.0-ubuntu20.04` |
| ![pytorch2.1.0] ![python3.8] ![Poetry] ![cuda12.3.2] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.0-py3.8-cuda12.3.2-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.0-py3.8-cuda12.3.2-ubuntu20.04` |
| ![pytorch2.1.0] ![python3.10] ![Poetry] ![cuda12.2.2] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.0-py3.10-cuda12.2.2-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.0-py3.10-cuda12.2.2-ubuntu20.04` |
| ![pytorch2.1.0] ![python3.11] ![Poetry] ![cuda12.3.2] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.0-py3.11-cuda12.3.2-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.0-py3.11-cuda12.3.2-ubuntu22.04` |
| ![pytorch2.1.0] ![python3.11] ![Poetry] ![cuda12.1.0] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.0-py3.11-cuda12.1.0-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.0-py3.11-cuda12.1.0-ubuntu22.04` |
| ![pytorch2.1.0] ![python3.8] ![Poetry] ![cuda12.3.2] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.0-py3.8-cuda12.3.2-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.0-py3.8-cuda12.3.2-ubuntu22.04` |
| ![pytorch2.1.0] ![python3.10] ![Poetry] ![cuda12.0.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.0-py3.10-cuda12.0.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.0-py3.10-cuda12.0.0-ubuntu20.04` |
| ![pytorch2.1.0] ![python3.10] ![Poetry] ![cuda11.8.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.0-py3.10-cuda11.8.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.0-py3.10-cuda11.8.0-ubuntu20.04` |
| ![pytorch2.1.0] ![python3.9] ![Poetry] ![cuda12.2.2] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.0-py3.9-cuda12.2.2-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.0-py3.9-cuda12.2.2-ubuntu20.04` |
| ![pytorch2.1.0] ![python3.11] ![Poetry] ![cuda11.8.0] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.0-py3.11-cuda11.8.0-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.0-py3.11-cuda11.8.0-ubuntu22.04` |
| ![pytorch2.1.0] ![python3.9] ![Poetry] ![cuda12.2.2] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.0-py3.9-cuda12.2.2-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.0-py3.9-cuda12.2.2-ubuntu22.04` |
| ![pytorch2.1.0] ![python3.9] ![Poetry] ![cuda12.3.2] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.0-py3.9-cuda12.3.2-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.0-py3.9-cuda12.3.2-ubuntu20.04` |
| ![pytorch2.1.0] ![python3.11] ![Poetry] ![cuda12.3.2] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.0-py3.11-cuda12.3.2-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.0-py3.11-cuda12.3.2-ubuntu20.04` |
| ![pytorch2.1.0] ![python3.10] ![Poetry] ![cuda12.2.2] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.0-py3.10-cuda12.2.2-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.0-py3.10-cuda12.2.2-ubuntu22.04` |
| ![pytorch2.1.0] ![python3.9] ![Poetry] ![cuda12.0.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.0-py3.9-cuda12.0.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.0-py3.9-cuda12.0.0-ubuntu20.04` |
| ![pytorch2.1.0] ![python3.10] ![Poetry] ![cuda12.1.0] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.0-py3.10-cuda12.1.0-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.0-py3.10-cuda12.1.0-ubuntu22.04` |
| ![pytorch2.1.0] ![python3.10] ![Poetry] ![cuda12.3.2] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.0-py3.10-cuda12.3.2-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.0-py3.10-cuda12.3.2-ubuntu22.04` |
| ![pytorch2.1.0] ![python3.9] ![Poetry] ![cuda12.0.0] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.0-py3.9-cuda12.0.0-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.0-py3.9-cuda12.0.0-ubuntu22.04` |
| ![pytorch2.1.0] ![python3.8] ![Poetry] ![cuda12.1.0] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.0-py3.8-cuda12.1.0-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.0-py3.8-cuda12.1.0-ubuntu22.04` |
| ![pytorch2.1.0] ![python3.8] ![Poetry] ![cuda11.8.0] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.0-py3.8-cuda11.8.0-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.0-py3.8-cuda11.8.0-ubuntu22.04` |
| ![pytorch2.1.0] ![python3.9] ![Poetry] ![cuda12.3.2] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.0-py3.9-cuda12.3.2-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.0-py3.9-cuda12.3.2-ubuntu22.04` |
| ![pytorch2.1.0] ![python3.9] ![Poetry] ![cuda12.1.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.0-py3.9-cuda12.1.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.0-py3.9-cuda12.1.0-ubuntu20.04` |
| ![pytorch2.1.0] ![python3.10] ![Poetry] ![cuda12.1.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.0-py3.10-cuda12.1.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.0-py3.10-cuda12.1.0-ubuntu20.04` |
| ![pytorch2.1.0] ![python3.10] ![Poetry] ![cuda12.3.2] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.0-py3.10-cuda12.3.2-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.0-py3.10-cuda12.3.2-ubuntu20.04` |
| ![pytorch2.1.0] ![python3.8] ![Poetry] ![cuda12.0.0] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.0-py3.8-cuda12.0.0-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.0-py3.8-cuda12.0.0-ubuntu22.04` |
| ![pytorch2.1.0] ![python3.9] ![Poetry] ![cuda11.8.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.0-py3.9-cuda11.8.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.0-py3.9-cuda11.8.0-ubuntu20.04` |
| ![pytorch2.1.0] ![python3.10] ![Poetry] ![cuda11.8.0] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.0-py3.10-cuda11.8.0-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.0-py3.10-cuda11.8.0-ubuntu22.04` |
| ![pytorch2.1.0] ![python3.11] ![Poetry] ![cuda12.2.2] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.0-py3.11-cuda12.2.2-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.0-py3.11-cuda12.2.2-ubuntu20.04` |
| ![pytorch2.1.0] ![python3.9] ![Poetry] ![cuda11.8.0] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.0-py3.9-cuda11.8.0-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.0-py3.9-cuda11.8.0-ubuntu22.04` |
| ![pytorch2.1.0] ![python3.10] ![Poetry] ![cuda12.0.0] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.0-py3.10-cuda12.0.0-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.0-py3.10-cuda12.0.0-ubuntu22.04` |
| ![pytorch2.1.0] ![python3.8] ![Poetry] ![cuda12.2.2] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.0-py3.8-cuda12.2.2-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.0-py3.8-cuda12.2.2-ubuntu22.04` |
| ![pytorch2.1.0] ![python3.8] ![Poetry] ![cuda12.2.2] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.0-py3.8-cuda12.2.2-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.0-py3.8-cuda12.2.2-ubuntu20.04` |
| ![pytorch2.1.0] ![python3.11] ![Poetry] ![cuda11.8.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.1.0-py3.11-cuda11.8.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.1.0-py3.11-cuda11.8.0-ubuntu20.04` |
| ![pytorch2.0.1] ![python3.10] ![Poetry] ![cuda12.0.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.0.1-py3.10-cuda12.0.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.0.1-py3.10-cuda12.0.0-ubuntu20.04` |
| ![pytorch2.0.1] ![python3.10] ![Poetry] ![cuda11.7.1] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.0.1-py3.10-cuda11.7.1-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.0.1-py3.10-cuda11.7.1-ubuntu20.04` |
| ![pytorch2.0.1] ![python3.10] ![Poetry] ![cuda12.0.0] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.0.1-py3.10-cuda12.0.0-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.0.1-py3.10-cuda12.0.0-ubuntu22.04` |
| ![pytorch2.0.1] ![python3.8] ![Poetry] ![cuda11.8.0] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.0.1-py3.8-cuda11.8.0-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.0.1-py3.8-cuda11.8.0-ubuntu22.04` |
| ![pytorch2.0.1] ![python3.9] ![Poetry] ![cuda12.0.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.0.1-py3.9-cuda12.0.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.0.1-py3.9-cuda12.0.0-ubuntu20.04` |
| ![pytorch2.0.1] ![python3.8] ![Poetry] ![cuda11.7.1] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.0.1-py3.8-cuda11.7.1-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.0.1-py3.8-cuda11.7.1-ubuntu20.04` |
| ![pytorch2.0.1] ![python3.11] ![Poetry] ![cuda11.7.1] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.0.1-py3.11-cuda11.7.1-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.0.1-py3.11-cuda11.7.1-ubuntu22.04` |
| ![pytorch2.0.1] ![python3.8] ![Poetry] ![cuda12.0.0] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.0.1-py3.8-cuda12.0.0-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.0.1-py3.8-cuda12.0.0-ubuntu22.04` |
| ![pytorch2.0.1] ![python3.8] ![Poetry] ![cuda11.8.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.0.1-py3.8-cuda11.8.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.0.1-py3.8-cuda11.8.0-ubuntu20.04` |
| ![pytorch2.0.1] ![python3.10] ![Poetry] ![cuda11.8.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.0.1-py3.10-cuda11.8.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.0.1-py3.10-cuda11.8.0-ubuntu20.04` |
| ![pytorch2.0.1] ![python3.11] ![Poetry] ![cuda11.8.0] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.0.1-py3.11-cuda11.8.0-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.0.1-py3.11-cuda11.8.0-ubuntu22.04` |
| ![pytorch2.0.1] ![python3.9] ![Poetry] ![cuda11.8.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.0.1-py3.9-cuda11.8.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.0.1-py3.9-cuda11.8.0-ubuntu20.04` |
| ![pytorch2.0.1] ![python3.8] ![Poetry] ![cuda12.0.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.0.1-py3.8-cuda12.0.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.0.1-py3.8-cuda12.0.0-ubuntu20.04` |
| ![pytorch2.0.1] ![python3.10] ![Poetry] ![cuda11.7.1] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.0.1-py3.10-cuda11.7.1-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.0.1-py3.10-cuda11.7.1-ubuntu22.04` |
| ![pytorch2.0.1] ![python3.9] ![Poetry] ![cuda11.8.0] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.0.1-py3.9-cuda11.8.0-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.0.1-py3.9-cuda11.8.0-ubuntu22.04` |
| ![pytorch2.0.1] ![python3.9] ![Poetry] ![cuda12.0.0] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.0.1-py3.9-cuda12.0.0-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.0.1-py3.9-cuda12.0.0-ubuntu22.04` |
| ![pytorch2.0.1] ![python3.10] ![Poetry] ![cuda11.8.0] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.0.1-py3.10-cuda11.8.0-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.0.1-py3.10-cuda11.8.0-ubuntu22.04` |
| ![pytorch2.0.1] ![python3.11] ![Poetry] ![cuda11.8.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.0.1-py3.11-cuda11.8.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.0.1-py3.11-cuda11.8.0-ubuntu20.04` |
| ![pytorch2.0.1] ![python3.11] ![Poetry] ![cuda12.0.0] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.0.1-py3.11-cuda12.0.0-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.0.1-py3.11-cuda12.0.0-ubuntu22.04` |
| ![pytorch2.0.1] ![python3.8] ![Poetry] ![cuda11.7.1] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.0.1-py3.8-cuda11.7.1-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.0.1-py3.8-cuda11.7.1-ubuntu22.04` |
| ![pytorch2.0.1] ![python3.11] ![Poetry] ![cuda12.0.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.0.1-py3.11-cuda12.0.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.0.1-py3.11-cuda12.0.0-ubuntu20.04` |
| ![pytorch2.0.1] ![python3.9] ![Poetry] ![cuda11.7.1] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.0.1-py3.9-cuda11.7.1-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.0.1-py3.9-cuda11.7.1-ubuntu22.04` |
| ![pytorch2.0.1] ![python3.9] ![Poetry] ![cuda11.7.1] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.0.1-py3.9-cuda11.7.1-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.0.1-py3.9-cuda11.7.1-ubuntu20.04` |
| ![pytorch2.0.1] ![python3.11] ![Poetry] ![cuda11.7.1] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.0.1-py3.11-cuda11.7.1-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.0.1-py3.11-cuda11.7.1-ubuntu20.04` |
| ![pytorch2.0.0] ![python3.10] ![Poetry] ![cuda11.7.1] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.0.0-py3.10-cuda11.7.1-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.0.0-py3.10-cuda11.7.1-ubuntu20.04` |
| ![pytorch2.0.0] ![python3.11] ![Poetry] ![cuda11.8.0] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.0.0-py3.11-cuda11.8.0-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.0.0-py3.11-cuda11.8.0-ubuntu22.04` |
| ![pytorch2.0.0] ![python3.9] ![Poetry] ![cuda11.8.0] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.0.0-py3.9-cuda11.8.0-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.0.0-py3.9-cuda11.8.0-ubuntu22.04` |
| ![pytorch2.0.0] ![python3.9] ![Poetry] ![cuda12.0.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.0.0-py3.9-cuda12.0.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.0.0-py3.9-cuda12.0.0-ubuntu20.04` |
| ![pytorch2.0.0] ![python3.8] ![Poetry] ![cuda11.7.1] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.0.0-py3.8-cuda11.7.1-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.0.0-py3.8-cuda11.7.1-ubuntu22.04` |
| ![pytorch2.0.0] ![python3.10] ![Poetry] ![cuda12.0.0] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.0.0-py3.10-cuda12.0.0-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.0.0-py3.10-cuda12.0.0-ubuntu22.04` |
| ![pytorch2.0.0] ![python3.8] ![Poetry] ![cuda11.7.1] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.0.0-py3.8-cuda11.7.1-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.0.0-py3.8-cuda11.7.1-ubuntu20.04` |
| ![pytorch2.0.0] ![python3.9] ![Poetry] ![cuda11.8.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.0.0-py3.9-cuda11.8.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.0.0-py3.9-cuda11.8.0-ubuntu20.04` |
| ![pytorch2.0.0] ![python3.9] ![Poetry] ![cuda12.0.0] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.0.0-py3.9-cuda12.0.0-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.0.0-py3.9-cuda12.0.0-ubuntu22.04` |
| ![pytorch2.0.0] ![python3.9] ![Poetry] ![cuda11.7.1] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.0.0-py3.9-cuda11.7.1-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.0.0-py3.9-cuda11.7.1-ubuntu20.04` |
| ![pytorch2.0.0] ![python3.8] ![Poetry] ![cuda11.8.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.0.0-py3.8-cuda11.8.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.0.0-py3.8-cuda11.8.0-ubuntu20.04` |
| ![pytorch2.0.0] ![python3.10] ![Poetry] ![cuda11.8.0] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.0.0-py3.10-cuda11.8.0-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.0.0-py3.10-cuda11.8.0-ubuntu22.04` |
| ![pytorch2.0.0] ![python3.10] ![Poetry] ![cuda11.7.1] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.0.0-py3.10-cuda11.7.1-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.0.0-py3.10-cuda11.7.1-ubuntu22.04` |
| ![pytorch2.0.0] ![python3.11] ![Poetry] ![cuda11.7.1] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.0.0-py3.11-cuda11.7.1-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.0.0-py3.11-cuda11.7.1-ubuntu20.04` |
| ![pytorch2.0.0] ![python3.11] ![Poetry] ![cuda12.0.0] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.0.0-py3.11-cuda12.0.0-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.0.0-py3.11-cuda12.0.0-ubuntu22.04` |
| ![pytorch2.0.0] ![python3.9] ![Poetry] ![cuda11.7.1] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.0.0-py3.9-cuda11.7.1-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.0.0-py3.9-cuda11.7.1-ubuntu22.04` |
| ![pytorch2.0.0] ![python3.8] ![Poetry] ![cuda12.0.0] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.0.0-py3.8-cuda12.0.0-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.0.0-py3.8-cuda12.0.0-ubuntu22.04` |
| ![pytorch2.0.0] ![python3.10] ![Poetry] ![cuda11.8.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.0.0-py3.10-cuda11.8.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.0.0-py3.10-cuda11.8.0-ubuntu20.04` |
| ![pytorch2.0.0] ![python3.8] ![Poetry] ![cuda12.0.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.0.0-py3.8-cuda12.0.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.0.0-py3.8-cuda12.0.0-ubuntu20.04` |
| ![pytorch2.0.0] ![python3.10] ![Poetry] ![cuda12.0.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.0.0-py3.10-cuda12.0.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.0.0-py3.10-cuda12.0.0-ubuntu20.04` |
| ![pytorch2.0.0] ![python3.11] ![Poetry] ![cuda12.0.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.0.0-py3.11-cuda12.0.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.0.0-py3.11-cuda12.0.0-ubuntu20.04` |
| ![pytorch2.0.0] ![python3.11] ![Poetry] ![cuda11.8.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.0.0-py3.11-cuda11.8.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.0.0-py3.11-cuda11.8.0-ubuntu20.04` |
| ![pytorch2.0.0] ![python3.11] ![Poetry] ![cuda11.7.1] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.0.0-py3.11-cuda11.7.1-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.0.0-py3.11-cuda11.7.1-ubuntu22.04` |
| ![pytorch2.0.0] ![python3.8] ![Poetry] ![cuda11.8.0] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/2.0.0-py3.8-cuda11.8.0-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/2.0.0-py3.8-cuda11.8.0-ubuntu22.04` |
| ![pytorch1.9.1] ![python3.8] ![Poetry] ![cuda11.1.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.9.1-py3.8-cuda11.1.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.9.1-py3.8-cuda11.1.0-ubuntu20.04` |
| ![pytorch1.9.1] ![python3.7] ![Pip] ![cuda11.1.1] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.9.1-py3.7-cuda11.1.1-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.9.1-py3.7-cuda11.1.1-ubuntu20.04` |
| ![pytorch1.9.1] ![python3.6] ![Pip] ![cuda11.1.1] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.9.1-py3.6-cuda11.1.1-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.9.1-py3.6-cuda11.1.1-ubuntu20.04` |
| ![pytorch1.9.1] ![python3.9] ![Poetry] ![cuda11.1.1] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.9.1-py3.9-cuda11.1.1-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.9.1-py3.9-cuda11.1.1-ubuntu20.04` |
| ![pytorch1.9.1] ![python3.6] ![Pip] ![cuda11.1.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.9.1-py3.6-cuda11.1.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.9.1-py3.6-cuda11.1.0-ubuntu20.04` |
| ![pytorch1.9.1] ![python3.8] ![Poetry] ![cuda11.1.1] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.9.1-py3.8-cuda11.1.1-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.9.1-py3.8-cuda11.1.1-ubuntu20.04` |
| ![pytorch1.9.1] ![python3.9] ![Poetry] ![cuda11.1.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.9.1-py3.9-cuda11.1.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.9.1-py3.9-cuda11.1.0-ubuntu20.04` |
| ![pytorch1.9.1] ![python3.7] ![Pip] ![cuda11.1.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.9.1-py3.7-cuda11.1.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.9.1-py3.7-cuda11.1.0-ubuntu20.04` |
| ![pytorch1.9.0] ![python3.8] ![Poetry] ![cuda11.1.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.9.0-py3.8-cuda11.1.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.9.0-py3.8-cuda11.1.0-ubuntu20.04` |
| ![pytorch1.9.0] ![python3.6] ![Pip] ![cuda11.1.1] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.9.0-py3.6-cuda11.1.1-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.9.0-py3.6-cuda11.1.1-ubuntu20.04` |
| ![pytorch1.9.0] ![python3.9] ![Poetry] ![cuda11.1.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.9.0-py3.9-cuda11.1.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.9.0-py3.9-cuda11.1.0-ubuntu20.04` |
| ![pytorch1.9.0] ![python3.9] ![Poetry] ![cuda11.1.1] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.9.0-py3.9-cuda11.1.1-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.9.0-py3.9-cuda11.1.1-ubuntu20.04` |
| ![pytorch1.9.0] ![python3.7] ![Pip] ![cuda11.1.1] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.9.0-py3.7-cuda11.1.1-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.9.0-py3.7-cuda11.1.1-ubuntu20.04` |
| ![pytorch1.9.0] ![python3.6] ![Pip] ![cuda11.1.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.9.0-py3.6-cuda11.1.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.9.0-py3.6-cuda11.1.0-ubuntu20.04` |
| ![pytorch1.9.0] ![python3.8] ![Poetry] ![cuda11.1.1] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.9.0-py3.8-cuda11.1.1-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.9.0-py3.8-cuda11.1.1-ubuntu20.04` |
| ![pytorch1.9.0] ![python3.7] ![Pip] ![cuda11.1.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.9.0-py3.7-cuda11.1.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.9.0-py3.7-cuda11.1.0-ubuntu20.04` |
| ![pytorch1.8.1] ![python3.6] ![Pip] ![cuda11.1.1] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.8.1-py3.6-cuda11.1.1-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.8.1-py3.6-cuda11.1.1-ubuntu20.04` |
| ![pytorch1.8.1] ![python3.8] ![Poetry] ![cuda11.1.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.8.1-py3.8-cuda11.1.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.8.1-py3.8-cuda11.1.0-ubuntu20.04` |
| ![pytorch1.8.1] ![python3.8] ![Poetry] ![cuda11.1.1] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.8.1-py3.8-cuda11.1.1-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.8.1-py3.8-cuda11.1.1-ubuntu20.04` |
| ![pytorch1.8.1] ![python3.6] ![Pip] ![cuda11.1.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.8.1-py3.6-cuda11.1.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.8.1-py3.6-cuda11.1.0-ubuntu20.04` |
| ![pytorch1.8.1] ![python3.9] ![Poetry] ![cuda11.1.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.8.1-py3.9-cuda11.1.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.8.1-py3.9-cuda11.1.0-ubuntu20.04` |
| ![pytorch1.8.1] ![python3.7] ![Pip] ![cuda11.1.1] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.8.1-py3.7-cuda11.1.1-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.8.1-py3.7-cuda11.1.1-ubuntu20.04` |
| ![pytorch1.8.1] ![python3.9] ![Poetry] ![cuda11.1.1] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.8.1-py3.9-cuda11.1.1-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.8.1-py3.9-cuda11.1.1-ubuntu20.04` |
| ![pytorch1.8.1] ![python3.7] ![Pip] ![cuda11.1.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.8.1-py3.7-cuda11.1.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.8.1-py3.7-cuda11.1.0-ubuntu20.04` |
| ![pytorch1.8.0] ![python3.8] ![Poetry] ![cuda11.1.1] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.8.0-py3.8-cuda11.1.1-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.8.0-py3.8-cuda11.1.1-ubuntu20.04` |
| ![pytorch1.8.0] ![python3.8] ![Poetry] ![cuda11.1.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.8.0-py3.8-cuda11.1.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.8.0-py3.8-cuda11.1.0-ubuntu20.04` |
| ![pytorch1.8.0] ![python3.9] ![Poetry] ![cuda11.1.1] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.8.0-py3.9-cuda11.1.1-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.8.0-py3.9-cuda11.1.1-ubuntu20.04` |
| ![pytorch1.8.0] ![python3.7] ![Pip] ![cuda11.1.1] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.8.0-py3.7-cuda11.1.1-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.8.0-py3.7-cuda11.1.1-ubuntu20.04` |
| ![pytorch1.8.0] ![python3.6] ![Pip] ![cuda11.1.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.8.0-py3.6-cuda11.1.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.8.0-py3.6-cuda11.1.0-ubuntu20.04` |
| ![pytorch1.8.0] ![python3.7] ![Pip] ![cuda11.1.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.8.0-py3.7-cuda11.1.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.8.0-py3.7-cuda11.1.0-ubuntu20.04` |
| ![pytorch1.8.0] ![python3.6] ![Pip] ![cuda11.1.1] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.8.0-py3.6-cuda11.1.1-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.8.0-py3.6-cuda11.1.1-ubuntu20.04` |
| ![pytorch1.8.0] ![python3.9] ![Poetry] ![cuda11.1.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.8.0-py3.9-cuda11.1.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.8.0-py3.9-cuda11.1.0-ubuntu20.04` |
| ![pytorch1.7.1] ![python3.7] ![Pip] ![cuda11.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.7.1-py3.7-cuda11.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.7.1-py3.7-cuda11.0-ubuntu20.04` |
| ![pytorch1.7.1] ![python3.8] ![Poetry] ![cuda11.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.7.1-py3.8-cuda11.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.7.1-py3.8-cuda11.0-ubuntu20.04` |
| ![pytorch1.7.1] ![python3.6] ![Pip] ![cuda11.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.7.1-py3.6-cuda11.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.7.1-py3.6-cuda11.0-ubuntu20.04` |
| ![pytorch1.7.1] ![python3.9] ![Poetry] ![cuda11.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.7.1-py3.9-cuda11.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.7.1-py3.9-cuda11.0-ubuntu20.04` |
| ![pytorch1.7.0] ![python3.8] ![Poetry] ![cuda11.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.7.0-py3.8-cuda11.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.7.0-py3.8-cuda11.0-ubuntu20.04` |
| ![pytorch1.7.0] ![python3.7] ![Pip] ![cuda11.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.7.0-py3.7-cuda11.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.7.0-py3.7-cuda11.0-ubuntu20.04` |
| ![pytorch1.7.0] ![python3.6] ![Pip] ![cuda11.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.7.0-py3.6-cuda11.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.7.0-py3.6-cuda11.0-ubuntu20.04` |
| ![pytorch1.13.1] ![python3.11] ![Poetry] ![cuda11.7.1] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.13.1-py3.11-cuda11.7.1-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.13.1-py3.11-cuda11.7.1-ubuntu22.04` |
| ![pytorch1.13.1] ![python3.10] ![Poetry] ![cuda11.7.1] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.13.1-py3.10-cuda11.7.1-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.13.1-py3.10-cuda11.7.1-ubuntu20.04` |
| ![pytorch1.13.1] ![python3.9] ![Poetry] ![cuda11.6.2] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.13.1-py3.9-cuda11.6.2-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.13.1-py3.9-cuda11.6.2-ubuntu20.04` |
| ![pytorch1.13.1] ![python3.8] ![Poetry] ![cuda11.7.1] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.13.1-py3.8-cuda11.7.1-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.13.1-py3.8-cuda11.7.1-ubuntu22.04` |
| ![pytorch1.13.1] ![python3.11] ![Poetry] ![cuda11.6.2] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.13.1-py3.11-cuda11.6.2-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.13.1-py3.11-cuda11.6.2-ubuntu20.04` |
| ![pytorch1.13.1] ![python3.10] ![Poetry] ![cuda11.6.2] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.13.1-py3.10-cuda11.6.2-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.13.1-py3.10-cuda11.6.2-ubuntu20.04` |
| ![pytorch1.13.1] ![python3.10] ![Poetry] ![cuda11.7.1] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.13.1-py3.10-cuda11.7.1-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.13.1-py3.10-cuda11.7.1-ubuntu22.04` |
| ![pytorch1.13.1] ![python3.7] ![Pip] ![cuda11.7.1] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.13.1-py3.7-cuda11.7.1-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.13.1-py3.7-cuda11.7.1-ubuntu20.04` |
| ![pytorch1.13.1] ![python3.7] ![Pip] ![cuda11.7.1] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.13.1-py3.7-cuda11.7.1-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.13.1-py3.7-cuda11.7.1-ubuntu22.04` |
| ![pytorch1.13.1] ![python3.8] ![Poetry] ![cuda11.6.2] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.13.1-py3.8-cuda11.6.2-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.13.1-py3.8-cuda11.6.2-ubuntu20.04` |
| ![pytorch1.13.1] ![python3.11] ![Poetry] ![cuda11.7.1] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.13.1-py3.11-cuda11.7.1-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.13.1-py3.11-cuda11.7.1-ubuntu20.04` |
| ![pytorch1.13.1] ![python3.7] ![Pip] ![cuda11.6.2] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.13.1-py3.7-cuda11.6.2-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.13.1-py3.7-cuda11.6.2-ubuntu20.04` |
| ![pytorch1.13.1] ![python3.8] ![Poetry] ![cuda11.7.1] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.13.1-py3.8-cuda11.7.1-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.13.1-py3.8-cuda11.7.1-ubuntu20.04` |
| ![pytorch1.13.1] ![python3.9] ![Poetry] ![cuda11.7.1] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.13.1-py3.9-cuda11.7.1-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.13.1-py3.9-cuda11.7.1-ubuntu22.04` |
| ![pytorch1.13.1] ![python3.9] ![Poetry] ![cuda11.7.1] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.13.1-py3.9-cuda11.7.1-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.13.1-py3.9-cuda11.7.1-ubuntu20.04` |
| ![pytorch1.13.0] ![python3.9] ![Poetry] ![cuda11.7.1] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.13.0-py3.9-cuda11.7.1-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.13.0-py3.9-cuda11.7.1-ubuntu22.04` |
| ![pytorch1.13.0] ![python3.9] ![Poetry] ![cuda11.7.1] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.13.0-py3.9-cuda11.7.1-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.13.0-py3.9-cuda11.7.1-ubuntu20.04` |
| ![pytorch1.13.0] ![python3.8] ![Poetry] ![cuda11.7.1] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.13.0-py3.8-cuda11.7.1-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.13.0-py3.8-cuda11.7.1-ubuntu22.04` |
| ![pytorch1.13.0] ![python3.10] ![Poetry] ![cuda11.7.1] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.13.0-py3.10-cuda11.7.1-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.13.0-py3.10-cuda11.7.1-ubuntu20.04` |
| ![pytorch1.13.0] ![python3.8] ![Poetry] ![cuda11.6.2] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.13.0-py3.8-cuda11.6.2-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.13.0-py3.8-cuda11.6.2-ubuntu20.04` |
| ![pytorch1.13.0] ![python3.7] ![Pip] ![cuda11.7.1] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.13.0-py3.7-cuda11.7.1-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.13.0-py3.7-cuda11.7.1-ubuntu22.04` |
| ![pytorch1.13.0] ![python3.8] ![Poetry] ![cuda11.7.1] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.13.0-py3.8-cuda11.7.1-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.13.0-py3.8-cuda11.7.1-ubuntu20.04` |
| ![pytorch1.13.0] ![python3.9] ![Poetry] ![cuda11.6.2] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.13.0-py3.9-cuda11.6.2-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.13.0-py3.9-cuda11.6.2-ubuntu20.04` |
| ![pytorch1.13.0] ![python3.10] ![Poetry] ![cuda11.7.1] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.13.0-py3.10-cuda11.7.1-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.13.0-py3.10-cuda11.7.1-ubuntu22.04` |
| ![pytorch1.13.0] ![python3.7] ![Pip] ![cuda11.7.1] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.13.0-py3.7-cuda11.7.1-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.13.0-py3.7-cuda11.7.1-ubuntu20.04` |
| ![pytorch1.13.0] ![python3.10] ![Poetry] ![cuda11.6.2] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.13.0-py3.10-cuda11.6.2-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.13.0-py3.10-cuda11.6.2-ubuntu20.04` |
| ![pytorch1.13.0] ![python3.7] ![Pip] ![cuda11.6.2] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.13.0-py3.7-cuda11.6.2-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.13.0-py3.7-cuda11.6.2-ubuntu20.04` |
| ![pytorch1.13.0] ![python3.11] ![Poetry] ![cuda11.7.1] ![ubuntu22.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.13.0-py3.11-cuda11.7.1-ubuntu22.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.13.0-py3.11-cuda11.7.1-ubuntu22.04` |
| ![pytorch1.13.0] ![python3.11] ![Poetry] ![cuda11.6.2] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.13.0-py3.11-cuda11.6.2-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.13.0-py3.11-cuda11.6.2-ubuntu20.04` |
| ![pytorch1.13.0] ![python3.11] ![Poetry] ![cuda11.7.1] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.13.0-py3.11-cuda11.7.1-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.13.0-py3.11-cuda11.7.1-ubuntu20.04` |
| ![pytorch1.12.1] ![python3.10] ![Poetry] ![cuda11.6.2] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.12.1-py3.10-cuda11.6.2-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.12.1-py3.10-cuda11.6.2-ubuntu20.04` |
| ![pytorch1.12.1] ![python3.9] ![Poetry] ![cuda11.3.1] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.12.1-py3.9-cuda11.3.1-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.12.1-py3.9-cuda11.3.1-ubuntu20.04` |
| ![pytorch1.12.1] ![python3.9] ![Poetry] ![cuda11.6.2] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.12.1-py3.9-cuda11.6.2-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.12.1-py3.9-cuda11.6.2-ubuntu20.04` |
| ![pytorch1.12.1] ![python3.7] ![Pip] ![cuda11.3.1] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.12.1-py3.7-cuda11.3.1-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.12.1-py3.7-cuda11.3.1-ubuntu20.04` |
| ![pytorch1.12.1] ![python3.8] ![Poetry] ![cuda11.3.1] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.12.1-py3.8-cuda11.3.1-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.12.1-py3.8-cuda11.3.1-ubuntu20.04` |
| ![pytorch1.12.1] ![python3.7] ![Pip] ![cuda11.6.2] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.12.1-py3.7-cuda11.6.2-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.12.1-py3.7-cuda11.6.2-ubuntu20.04` |
| ![pytorch1.12.1] ![python3.8] ![Poetry] ![cuda11.6.2] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.12.1-py3.8-cuda11.6.2-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.12.1-py3.8-cuda11.6.2-ubuntu20.04` |
| ![pytorch1.12.1] ![python3.10] ![Poetry] ![cuda11.3.1] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.12.1-py3.10-cuda11.3.1-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.12.1-py3.10-cuda11.3.1-ubuntu20.04` |
| ![pytorch1.12.0] ![python3.7] ![Pip] ![cuda11.6.2] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.12.0-py3.7-cuda11.6.2-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.12.0-py3.7-cuda11.6.2-ubuntu20.04` |
| ![pytorch1.12.0] ![python3.9] ![Poetry] ![cuda11.3.1] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.12.0-py3.9-cuda11.3.1-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.12.0-py3.9-cuda11.3.1-ubuntu20.04` |
| ![pytorch1.12.0] ![python3.10] ![Poetry] ![cuda11.6.2] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.12.0-py3.10-cuda11.6.2-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.12.0-py3.10-cuda11.6.2-ubuntu20.04` |
| ![pytorch1.12.0] ![python3.7] ![Pip] ![cuda11.3.1] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.12.0-py3.7-cuda11.3.1-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.12.0-py3.7-cuda11.3.1-ubuntu20.04` |
| ![pytorch1.12.0] ![python3.8] ![Poetry] ![cuda11.3.1] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.12.0-py3.8-cuda11.3.1-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.12.0-py3.8-cuda11.3.1-ubuntu20.04` |
| ![pytorch1.12.0] ![python3.10] ![Poetry] ![cuda11.3.1] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.12.0-py3.10-cuda11.3.1-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.12.0-py3.10-cuda11.3.1-ubuntu20.04` |
| ![pytorch1.12.0] ![python3.9] ![Poetry] ![cuda11.6.2] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.12.0-py3.9-cuda11.6.2-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.12.0-py3.9-cuda11.6.2-ubuntu20.04` |
| ![pytorch1.12.0] ![python3.8] ![Poetry] ![cuda11.6.2] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.12.0-py3.8-cuda11.6.2-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.12.0-py3.8-cuda11.6.2-ubuntu20.04` |
| ![pytorch1.11.0] ![python3.8] ![Poetry] ![cuda11.5.2] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.11.0-py3.8-cuda11.5.2-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.11.0-py3.8-cuda11.5.2-ubuntu20.04` |
| ![pytorch1.11.0] ![python3.8] ![Poetry] ![cuda11.3.1] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.11.0-py3.8-cuda11.3.1-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.11.0-py3.8-cuda11.3.1-ubuntu20.04` |
| ![pytorch1.11.0] ![python3.10] ![Poetry] ![cuda11.5.2] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.11.0-py3.10-cuda11.5.2-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.11.0-py3.10-cuda11.5.2-ubuntu20.04` |
| ![pytorch1.11.0] ![python3.7] ![Pip] ![cuda11.5.2] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.11.0-py3.7-cuda11.5.2-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.11.0-py3.7-cuda11.5.2-ubuntu20.04` |
| ![pytorch1.11.0] ![python3.9] ![Poetry] ![cuda11.3.1] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.11.0-py3.9-cuda11.3.1-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.11.0-py3.9-cuda11.3.1-ubuntu20.04` |
| ![pytorch1.11.0] ![python3.7] ![Pip] ![cuda11.3.1] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.11.0-py3.7-cuda11.3.1-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.11.0-py3.7-cuda11.3.1-ubuntu20.04` |
| ![pytorch1.11.0] ![python3.10] ![Poetry] ![cuda11.3.1] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.11.0-py3.10-cuda11.3.1-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.11.0-py3.10-cuda11.3.1-ubuntu20.04` |
| ![pytorch1.11.0] ![python3.9] ![Poetry] ![cuda11.5.2] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.11.0-py3.9-cuda11.5.2-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.11.0-py3.9-cuda11.5.2-ubuntu20.04` |
| ![pytorch1.10.2] ![python3.9] ![Poetry] ![cuda11.1.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.10.2-py3.9-cuda11.1.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.10.2-py3.9-cuda11.1.0-ubuntu20.04` |
| ![pytorch1.10.2] ![python3.7] ![Pip] ![cuda11.1.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.10.2-py3.7-cuda11.1.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.10.2-py3.7-cuda11.1.0-ubuntu20.04` |
| ![pytorch1.10.2] ![python3.8] ![Poetry] ![cuda11.1.1] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.10.2-py3.8-cuda11.1.1-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.10.2-py3.8-cuda11.1.1-ubuntu20.04` |
| ![pytorch1.10.2] ![python3.9] ![Poetry] ![cuda11.3.1] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.10.2-py3.9-cuda11.3.1-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.10.2-py3.9-cuda11.3.1-ubuntu20.04` |
| ![pytorch1.10.2] ![python3.7] ![Pip] ![cuda11.3.1] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.10.2-py3.7-cuda11.3.1-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.10.2-py3.7-cuda11.3.1-ubuntu20.04` |
| ![pytorch1.10.2] ![python3.7] ![Pip] ![cuda11.1.1] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.10.2-py3.7-cuda11.1.1-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.10.2-py3.7-cuda11.1.1-ubuntu20.04` |
| ![pytorch1.10.2] ![python3.8] ![Poetry] ![cuda11.1.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.10.2-py3.8-cuda11.1.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.10.2-py3.8-cuda11.1.0-ubuntu20.04` |
| ![pytorch1.10.2] ![python3.9] ![Poetry] ![cuda11.1.1] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.10.2-py3.9-cuda11.1.1-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.10.2-py3.9-cuda11.1.1-ubuntu20.04` |
| ![pytorch1.10.2] ![python3.6] ![Pip] ![cuda11.1.1] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.10.2-py3.6-cuda11.1.1-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.10.2-py3.6-cuda11.1.1-ubuntu20.04` |
| ![pytorch1.10.2] ![python3.6] ![Pip] ![cuda11.1.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.10.2-py3.6-cuda11.1.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.10.2-py3.6-cuda11.1.0-ubuntu20.04` |
| ![pytorch1.10.2] ![python3.6] ![Pip] ![cuda11.3.1] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.10.2-py3.6-cuda11.3.1-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.10.2-py3.6-cuda11.3.1-ubuntu20.04` |
| ![pytorch1.10.2] ![python3.8] ![Poetry] ![cuda11.3.1] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.10.2-py3.8-cuda11.3.1-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.10.2-py3.8-cuda11.3.1-ubuntu20.04` |
| ![pytorch1.10.1] ![python3.6] ![Pip] ![cuda11.1.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.10.1-py3.6-cuda11.1.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.10.1-py3.6-cuda11.1.0-ubuntu20.04` |
| ![pytorch1.10.1] ![python3.8] ![Poetry] ![cuda11.1.1] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.10.1-py3.8-cuda11.1.1-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.10.1-py3.8-cuda11.1.1-ubuntu20.04` |
| ![pytorch1.10.1] ![python3.6] ![Pip] ![cuda11.1.1] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.10.1-py3.6-cuda11.1.1-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.10.1-py3.6-cuda11.1.1-ubuntu20.04` |
| ![pytorch1.10.1] ![python3.6] ![Pip] ![cuda11.3.1] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.10.1-py3.6-cuda11.3.1-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.10.1-py3.6-cuda11.3.1-ubuntu20.04` |
| ![pytorch1.10.1] ![python3.9] ![Poetry] ![cuda11.1.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.10.1-py3.9-cuda11.1.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.10.1-py3.9-cuda11.1.0-ubuntu20.04` |
| ![pytorch1.10.1] ![python3.8] ![Poetry] ![cuda11.3.1] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.10.1-py3.8-cuda11.3.1-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.10.1-py3.8-cuda11.3.1-ubuntu20.04` |
| ![pytorch1.10.1] ![python3.7] ![Pip] ![cuda11.1.1] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.10.1-py3.7-cuda11.1.1-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.10.1-py3.7-cuda11.1.1-ubuntu20.04` |
| ![pytorch1.10.1] ![python3.8] ![Poetry] ![cuda11.1.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.10.1-py3.8-cuda11.1.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.10.1-py3.8-cuda11.1.0-ubuntu20.04` |
| ![pytorch1.10.1] ![python3.9] ![Poetry] ![cuda11.3.1] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.10.1-py3.9-cuda11.3.1-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.10.1-py3.9-cuda11.3.1-ubuntu20.04` |
| ![pytorch1.10.1] ![python3.7] ![Pip] ![cuda11.3.1] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.10.1-py3.7-cuda11.3.1-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.10.1-py3.7-cuda11.3.1-ubuntu20.04` |
| ![pytorch1.10.1] ![python3.7] ![Pip] ![cuda11.1.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.10.1-py3.7-cuda11.1.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.10.1-py3.7-cuda11.1.0-ubuntu20.04` |
| ![pytorch1.10.1] ![python3.9] ![Poetry] ![cuda11.1.1] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.10.1-py3.9-cuda11.1.1-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.10.1-py3.9-cuda11.1.1-ubuntu20.04` |
| ![pytorch1.10.0] ![python3.8] ![Poetry] ![cuda11.1.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.10.0-py3.8-cuda11.1.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.10.0-py3.8-cuda11.1.0-ubuntu20.04` |
| ![pytorch1.10.0] ![python3.8] ![Poetry] ![cuda11.3.1] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.10.0-py3.8-cuda11.3.1-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.10.0-py3.8-cuda11.3.1-ubuntu20.04` |
| ![pytorch1.10.0] ![python3.6] ![Pip] ![cuda11.1.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.10.0-py3.6-cuda11.1.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.10.0-py3.6-cuda11.1.0-ubuntu20.04` |
| ![pytorch1.10.0] ![python3.6] ![Pip] ![cuda11.1.1] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.10.0-py3.6-cuda11.1.1-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.10.0-py3.6-cuda11.1.1-ubuntu20.04` |
| ![pytorch1.10.0] ![python3.7] ![Pip] ![cuda11.1.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.10.0-py3.7-cuda11.1.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.10.0-py3.7-cuda11.1.0-ubuntu20.04` |
| ![pytorch1.10.0] ![python3.9] ![Poetry] ![cuda11.3.1] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.10.0-py3.9-cuda11.3.1-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.10.0-py3.9-cuda11.3.1-ubuntu20.04` |
| ![pytorch1.10.0] ![python3.9] ![Poetry] ![cuda11.1.1] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.10.0-py3.9-cuda11.1.1-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.10.0-py3.9-cuda11.1.1-ubuntu20.04` |
| ![pytorch1.10.0] ![python3.6] ![Pip] ![cuda11.3.1] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.10.0-py3.6-cuda11.3.1-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.10.0-py3.6-cuda11.3.1-ubuntu20.04` |
| ![pytorch1.10.0] ![python3.8] ![Poetry] ![cuda11.1.1] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.10.0-py3.8-cuda11.1.1-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.10.0-py3.8-cuda11.1.1-ubuntu20.04` |
| ![pytorch1.10.0] ![python3.7] ![Pip] ![cuda11.1.1] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.10.0-py3.7-cuda11.1.1-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.10.0-py3.7-cuda11.1.1-ubuntu20.04` |
| ![pytorch1.10.0] ![python3.9] ![Poetry] ![cuda11.1.0] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.10.0-py3.9-cuda11.1.0-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.10.0-py3.9-cuda11.1.0-ubuntu20.04` |
| ![pytorch1.10.0] ![python3.7] ![Pip] ![cuda11.3.1] ![ubuntu20.04] | [![](https://img.shields.io/docker/image-size/liuyuweitarek/pytorch/1.10.0-py3.7-cuda11.3.1-ubuntu20.04?style=plastic&label=Size)][DockerHub] | `docker pull liuyuweitarek/pytorch/1.10.0-py3.7-cuda11.3.1-ubuntu20.04` |

## Dependencies References

- CUDA Toolkit: 
  - cuda9.2: https://developer.nvidia.com/cuda-92-download-archive
  - cuda10.0: https://developer.nvidia.com/cuda-10.0-download-archive
  - cuda10.1: https://developer.nvidia.com/cuda-10.1-download-archive-base
  - cuda10.2: https://developer.nvidia.com/cuda-10.2-download-archive
  - cuda11.0: https://developer.nvidia.com/cuda-11.0-download-archive
  - cuda11.1.0: https://developer.nvidia.com/cuda-11.1.0-download-archive
  - cuda11.1.1: https://developer.nvidia.com/cuda-11.1.1-download-archive
  - cuda11.3.1: https://developer.nvidia.com/cuda-11-3-1-download-archive
  - cuda11.5.2: https://developer.nvidia.com/cuda-11-5-2-download-archive
  - cuda11.6.2: https://developer.nvidia.com/cuda-11-6-2-download-archive
  - cuda11.7.1: https://developer.nvidia.com/cuda-11-7-1-download-archive
  - cuda11.8.0: https://developer.nvidia.com/cuda-11-8-0-download-archive
  - cuda12.0.0: https://developer.nvidia.com/cuda-12-0-0-download-archive
  - cuda12.1.0: https://developer.nvidia.com/cuda-12-1-0-download-archive
  - cuda12.2.2: https://developer.nvidia.com/cuda-12-2-2-download-archive
  - cuda12.3.2: https://developer.nvidia.com/cuda-12-3-2-download-archive
  - cuda12.4.1: https://developer.nvidia.com/cuda-12-4-1-download-archive
  - cuda12.5.1: https://developer.nvidia.com/cuda-12-5-1-download-archive
  - cuda12.6.1: https://developer.nvidia.com/cuda-12-6-1-download-archive
    
- Pytorch: 
  - https://download.pytorch.org/whl/torch_stable.html

- Poetry(Only support for Python >=3.8): 
