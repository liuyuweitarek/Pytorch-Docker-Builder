import json
import requests
from typing import Union, List, Dict

from constants import SOURCE_FILE, META_FILE, ON_BUILDING_FILE, TARGET_FILE, ImageState

FORMAT_MSG = """Please format as:
[
  {
    'CUDA_VERSION': 'CUDA_TOOLKIT_VERSION',
    'CUDA_NAME': 'CUDA_NAME',
    'PYTHON_VERSION': 'PYTHON_VERSION',
    'TORCH_VERSION': 'TORCH_VERSION',
    'TORCH_PACKAGE_NAME': 'TORCH_VERSION+CUDA_NAME',
    'UBUNTU_VERSION': 'UBUNTU_VERSION',
  },
  ...
]"""

def read_json(filename: str) -> Union[dict, list]:
    
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"The file '{filename}' does not exist.")
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to decode JSON from '{filename}': {e}")
    except Exception as e:
        raise RuntimeError(f"An error occurred while reading '{filename}': {e}")


def write_json(data: Union[dict, list], filename: str, encoding: str = "utf-8") -> None:
    try:
        with open(filename, "w", encoding=encoding) as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except TypeError as e:
        raise ValueError(f"Provided data is not JSON serializable: {e}")
    except Exception as e:
        raise RuntimeError(f"An error occurred while writing to '{filename}': {e}")

def get_all_tags() -> dict:
    page = 1
    next_page_exist = True
    tags = []
    
    while next_page_exist:
        response = requests.get(f'https://hub.docker.com/v2/repositories/liuyuweitarek/pytorch/tags?page={page}&page_size=100')
        
        if response.status_code == 200:
            data = response.json()
            tags += [image["name"] for image in data["results"] if image["name"] != "update-readme"]
            next_page_exist = True if data['next'] is not None else False
            page += 1
        else:
            print(f"Error: {response.status_code} happened while getting all tags.")
            next_page_exist = False

    return tags

def tags_to_info(tag: str) -> dict:
    
    if tag == "update-readme":
        return None
    
    pytorch_version = tag[0:tag.index('-')]
    python_version = tag[(tag.index('py')+len('py')):tag.index('-', tag.index('py'), len(tag))]
    cuda_version = tag[(tag.index('cuda')+len('cuda')):tag.index('-', tag.index('cuda'), len(tag))]
    ubuntu_version = tag[(tag.index('ubuntu')+len('ubuntu'))::]

    return {
        'pytorch_version': pytorch_version,
        'python_version': python_version,
        'cuda_version': cuda_version,
        'ubuntu_version': ubuntu_version
    }

def get_dockerhub_state() -> dict:
    tags = get_all_tags()
    return list(map(tags_to_info, tags))

def prepare_compatible_versions(
    source_file: str = SOURCE_FILE,
    meta_file: str = META_FILE,
    on_building_file: str = ON_BUILDING_FILE,
    use_target_file: bool = False,
    target_file: str = TARGET_FILE,
) -> None:

    compatible_versions: List[Dict[str, str]] = []

    if use_target_file:
        target = read_json(target_file)
        if not target:
            raise ValueError(f"Target file '{target_file}' is empty. {FORMAT_MSG}")

        for target_version in target:
            if set(target_version.keys()) != set(["CUDA_VERSION", "CUDA_NAME", "PYTHON_VERSION", "TORCH_VERSION", "TORCH_PACKAGE_NAME", "UBUNTU_VERSION"]):
                raise ValueError(f"Target: '{target_version}' has wrong format. {FORMAT_MSG}")
        
        write_json(data=target, filename=on_building_file)
        return

    source = read_json(source_file)
    meta = read_json(meta_file)

    dockerhub_state = get_dockerhub_state()
    for image_info in dockerhub_state:
        source[image_info["cuda_version"]][image_info["ubuntu_version"]][image_info["python_version"]][image_info["pytorch_version"]][0] = ImageState.BUILD_SUCCESS

    for CUDA_TOOLKIT_VERSION, ubuntu_config in source.items():
        CUDA_NAME = meta[CUDA_TOOLKIT_VERSION]["package_name"]
        for UBUNTU_VERSION, python_config in ubuntu_config.items():
            for PYTHON_VERSION, torch_config in python_config.items():
                for TORCH_VERSION, image_states in torch_config.items():
                    if UBUNTU_VERSION < "20.04":
                        source[CUDA_TOOLKIT_VERSION][UBUNTU_VERSION][PYTHON_VERSION][TORCH_VERSION][0] = ImageState.PENDING
                        image_states[0] = ImageState.PENDING

                    if image_states[0] in [ImageState.NOT_BUILD_YET, ImageState.BUILD_FAILED]:
                        compatible_versions.append(
                            {
                                "CUDA_VERSION": CUDA_TOOLKIT_VERSION,
                                "CUDA_NAME": CUDA_NAME,
                                "PYTHON_VERSION": PYTHON_VERSION,
                                "TORCH_VERSION": TORCH_VERSION,
                                "TORCH_PACKAGE_NAME": f"{TORCH_VERSION}+{CUDA_NAME}",
                                "UBUNTU_VERSION": UBUNTU_VERSION,
                            }
                        )

    write_json(data=compatible_versions, filename=on_building_file)