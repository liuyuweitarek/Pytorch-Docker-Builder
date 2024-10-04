import re
import json
import argparse
import requests
from utils import read_json, write_json
from templates import readme_template, image_table_row_template, raw_image_table_row_template
from constants import BADGES_FILE, SOURCE_FILE, PYTHON_TAG, PYTORCH_TAG, CUDA_TAG, UBUNTU_TAG, LOCAL_PYTHON_TAG, LOCAL_PYTORCH_TAG, LOCAL_CUDA_TAG, LOCAL_UBUNTU_TAG, ImageState

def cache_badge(
    tag_url: str,
    tag_name: str
) -> None:
    
    global badge_set
    
    if tag_url in badge_set:
        return
    
    badge_set.add(tag_url)
    svg = requests.get(tag_url).text
    
    with open(f"badges/{tag_name}.svg", 'w') as f:
        f.write(svg)
    
    return
    

def update_source(args) -> None:
    pytorch_version = args.torch_version
    python_version = args.python_version
    cuda_version = args.cuda_version
    ubuntu_version = args.ubuntu_version
    build_result = args.build_result
    
    source = read_json(SOURCE_FILE)
    source[cuda_version][ubuntu_version][python_version][pytorch_version][0] = build_result
    
    write_json(data=source, filename=SOURCE_FILE)
    
def update_readme():
    
    global badge_set
    
    source = read_json(SOURCE_FILE)

    image_table_rows = []
    cuda_tags = set()
    ubuntu_tags = set()
    pytorch_tags = set()
    python_tags = set()
    
    for CUDA_TOOLKIT_VERSION, ubuntu_config in source.items():
        for UBUNTU_VERSION, python_config in ubuntu_config.items():
            for PYTHON_VERSION, torch_config in python_config.items():
                for TORCH_VERSION, image_states in torch_config.items():
                    cache_badge(
                        tag_name="cuda{}".format(CUDA_TOOLKIT_VERSION),
                        tag_url=CUDA_TAG.format(CUDA_VERSION=CUDA_TOOLKIT_VERSION)
                    )
                    cache_badge(
                        tag_name="ubuntu{}".format(UBUNTU_VERSION),
                        tag_url=UBUNTU_TAG.format(UBUNTU_VERSION=UBUNTU_VERSION)
                    )
                    cache_badge(
                        tag_name="python{}".format(PYTHON_VERSION),
                        tag_url=PYTHON_TAG.format(PYTHON_VERSION=PYTHON_VERSION)
                    )
                    cache_badge(
                        tag_name="pytorch{}".format(TORCH_VERSION),
                        tag_url=PYTORCH_TAG.format(TORCH_VERSION=TORCH_VERSION)
                    )

                    if image_states[0] == ImageState.BUILD_SUCCESS:
                        cuda_tags.add(LOCAL_CUDA_TAG.format(CUDA_VERSION=CUDA_TOOLKIT_VERSION))
                        ubuntu_tags.add(LOCAL_UBUNTU_TAG.format(UBUNTU_VERSION=UBUNTU_VERSION))
                        python_tags.add(LOCAL_PYTHON_TAG.format(PYTHON_VERSION=PYTHON_VERSION))
                        pytorch_tags.add(LOCAL_PYTORCH_TAG.format(TORCH_VERSION=TORCH_VERSION))
                        image_table_rows.append(
                            image_table_row_template.format(
                                CUDA_VERSION=CUDA_TOOLKIT_VERSION,
                                UBUNTU_VERSION=UBUNTU_VERSION,
                                PYTHON_VERSION=PYTHON_VERSION,
                                PACKAGE_MANAGEMENT="Poetry" if PYTHON_VERSION not in ["3.6", "3.7"] else "Pip",
                                TORCH_VERSION=TORCH_VERSION
                            )
                        ) 
    
    write_json(list(badge_set), BADGES_FILE)

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


if __name__ == "__main__":
    badge_set = set(read_json(BADGES_FILE))
    # python report.py  -t test-tag --torch-version 2.1.0 --python-version 3.8 --cuda-version 11.8.0 --ubuntu-version 20.04 --build-result "Build Success"
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-t", "--tag", type=str, required=True, 
                        help="Docker image full name to push, which should be formatted as: \n"
                            "<docker_hub_username>/<repo>:<tag>. \n"
                            "e.g. liuyuweitarek/pytorch:1.12.0-py3.10-cuda11.3-ubuntu20.04")
    parser.add_argument("--torch-version", type=str, required=True, help="The torch version for the image.")
    parser.add_argument("--python-version", type=str, required=True, help="The python version for the image.")
    parser.add_argument("--cuda-version", type=str, required=True, help="The cuda version for the image.")
    parser.add_argument("--ubuntu-version", type=str, required=True, help="The ubuntu version for the image.")
    parser.add_argument("--build-result", type=str, required=True, help="The result of the built image.")
    args = parser.parse_args()
    
    update_source(args)
    update_readme()

    