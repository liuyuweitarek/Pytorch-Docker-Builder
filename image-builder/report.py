import os
import requests
from utils import get_dockerhub_state
from templates import readme_template, image_table_row_template, raw_image_table_row_template
from constants import BADGES_DIR, SOURCE_FILE, PYTHON_TAG, PYTORCH_TAG, CUDA_TAG, UBUNTU_TAG, LOCAL_PYTHON_TAG, LOCAL_PYTORCH_TAG, LOCAL_CUDA_TAG, LOCAL_UBUNTU_TAG, ImageState

def cache_badge(
    tag_url: str,
    tag_name: str
) -> None:
    
    if os.path.exists(f"{BADGES_DIR}/{tag_name}.svg"):
        return
    
    svg = requests.get(tag_url).text
    
    with open(f"{BADGES_DIR}/{tag_name}.svg", 'w') as f:
        f.write(svg)

def update_readme_beta():

    image_table_rows = []
    cuda_tags = set()
    ubuntu_tags = set()
    pytorch_tags = set()
    python_tags = set()

    dockerhub_state = sorted(get_dockerhub_state(), key=lambda d: d['pytorch_version'], reverse=True)

    for image_info in dockerhub_state:
        cache_badge(
            tag_name="cuda{}".format(image_info["cuda_version"]),
            tag_url=CUDA_TAG.format(CUDA_VERSION=image_info["cuda_version"])
        )
        cache_badge(
            tag_name="ubuntu{}".format(image_info["ubuntu_version"]),
            tag_url=UBUNTU_TAG.format(UBUNTU_VERSION=image_info["ubuntu_version"])
        )
        cache_badge(
            tag_name="python{}".format(image_info["python_version"]),
            tag_url=PYTHON_TAG.format(PYTHON_VERSION=image_info["python_version"])
        )
        cache_badge(
            tag_name="pytorch{}".format(image_info["pytorch_version"]),
            tag_url=PYTORCH_TAG.format(TORCH_VERSION=image_info["pytorch_version"])
        )
        cuda_tags.add(LOCAL_CUDA_TAG.format(CUDA_VERSION=image_info["cuda_version"]))
        ubuntu_tags.add(LOCAL_UBUNTU_TAG.format(UBUNTU_VERSION=image_info["ubuntu_version"]))
        python_tags.add(LOCAL_PYTHON_TAG.format(PYTHON_VERSION=image_info["python_version"]))
        pytorch_tags.add(LOCAL_PYTORCH_TAG.format(TORCH_VERSION=image_info["pytorch_version"]))
        image_table_rows.append(
            image_table_row_template.format(
                CUDA_VERSION=image_info["cuda_version"],
                UBUNTU_VERSION=image_info["ubuntu_version"],
                PYTHON_VERSION=image_info["python_version"],
                PACKAGE_MANAGEMENT="Poetry" if image_info["python_version"] not in ["3.6", "3.7"] else "Pip",
                TORCH_VERSION=image_info["pytorch_version"]
            )
        ) 

    with open("../README.md", "w", encoding="utf-8") as f:
        f.write(
            readme_template.format(
                CUDA_TAGS="\n".join(sorted(cuda_tags, key=lambda x: list(map(int, x[x.index('cuda')+4:x.index(']')].split('.'))), reverse=True)),
                UBUNTU_TAGS="\n".join(sorted(ubuntu_tags, reverse=True)),
                PYTORCH_TAGS="\n".join(sorted(pytorch_tags, reverse=True)),
                PYTHON_TAGS="\n".join(sorted(python_tags, key=lambda x: list(map(int, x[x.index('python')+6:x.index(']')].split('.'))), reverse=True)),
                IMAGE_TABLE="\n".join(reversed(image_table_rows))
            )
        )

    