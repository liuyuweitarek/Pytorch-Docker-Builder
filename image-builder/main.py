import os
from constants import BADGES_DIR, GITHUB_WORKFLOW_DIR, PYPROJECT_TOML_DIR, LOCAL_BUILD_SCRIPTS_DIR, TARGET_FILE, ON_BUILDING_FILE, TORCH_SOURCE_URL
from templates import pyproject_toml_template, github_workflow_template, local_poetry_build_script_template, local_pip_build_script_template
from utils import prepare_compatible_versions, read_json, write_json

prepare_compatible_versions()

os.makedirs(f"../{GITHUB_WORKFLOW_DIR}", exist_ok=True)
os.makedirs(f"../{LOCAL_BUILD_SCRIPTS_DIR}", exist_ok=True)
os.makedirs(PYPROJECT_TOML_DIR, exist_ok=True)
os.makedirs(BADGES_DIR, exist_ok=True)

compatible_versions = read_json(ON_BUILDING_FILE)

for version_info in compatible_versions:
    locals().update(version_info)
    
    tag = (
        f"{TORCH_VERSION}-py{PYTHON_VERSION}-cuda{CUDA_VERSION}-ubuntu{UBUNTU_VERSION}"
    )
    torch_source_url = TORCH_SOURCE_URL.format(CUDA_NAME=CUDA_NAME)
    IMAGE_TAG = f"liuyuweitarek/pytorch:{tag}"
    pyproject_filename = ""
    workflow_filename = f"docker_build_pytorch{tag}.yml"
    local_build_script_filename = f"build_{tag}.sh"
    
    # Generate pyproject.toml
    if PYTHON_VERSION not in ["3.6", "3.7"]:
        pyproject_filename = f"pytorch{tag}.toml"

        with open(os.path.join(PYPROJECT_TOML_DIR, pyproject_filename), "w", encoding="utf-8") as f:
            f.write(
                pyproject_toml_template.format(
                    PYTHON_VERSION=PYTHON_VERSION,
                    TORCH_PACKAGE_NAME=TORCH_PACKAGE_NAME,
                    TORCH_SOURCE_URL=torch_source_url,
                )
            )
    
    # Generate local test scripts
    with open(os.path.join(f"../{LOCAL_BUILD_SCRIPTS_DIR}", local_build_script_filename), "w", encoding="utf-8") as f:
        # Poetry
        if PYTHON_VERSION not in ["3.6", "3.7"]:
            f.write(
                local_poetry_build_script_template.format(
                    IMAGE_TAG=IMAGE_TAG,
                    PYTHON_VERSION=PYTHON_VERSION,
                    PYPROJECT_FILE_DIR="image-builder/docker/default-workspace",
                    DEFAULT_PYPROJECT_FILE=pyproject_filename,
                    UBUNTU_VERSION=UBUNTU_VERSION,
                )
            )
        # Pip
        else: 
            f.write(
                local_pip_build_script_template.format(
                    IMAGE_TAG=IMAGE_TAG,
                    PYTHON_VERSION=PYTHON_VERSION,
                    TORCH_PACKAGE_NAME=TORCH_PACKAGE_NAME,
                    TORCH_SOURCE_URL=torch_source_url,
                    UBUNTU_VERSION=UBUNTU_VERSION,
                )
            )
        os.system('chmod +x {}'.format(os.path.join(f"../{LOCAL_BUILD_SCRIPTS_DIR}", local_build_script_filename)))

    # Generate workflow.yml
    with open(os.path.join(f"../{GITHUB_WORKFLOW_DIR}", workflow_filename), "w", encoding="utf-8") as f:
        
        f.write(
            github_workflow_template.format(
                IMAGE_TAG=IMAGE_TAG,
                PACKAGE_MANAGEMENT = "poetry" if PYTHON_VERSION not in ["3.6", "3.7"] else "pip",
                PYTHON_VERSION=PYTHON_VERSION,
                TORCH_VERSION=TORCH_VERSION,
                TORCH_PACKAGE_NAME=TORCH_PACKAGE_NAME,
                TORCH_SOURCE_URL=torch_source_url,
                PYPROJECT_FILE_DIR="./default-workspace",
                DEFAULT_PYPROJECT_FILE=pyproject_filename,
                CUDA_VERSION=CUDA_VERSION,
                UBUNTU_VERSION=UBUNTU_VERSION,
                WORKFLOW_FILE=os.path.join(GITHUB_WORKFLOW_DIR, workflow_filename)
            )
        )
