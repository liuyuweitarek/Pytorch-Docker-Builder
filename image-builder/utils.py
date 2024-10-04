import json
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

    for CUDA_TOOLKIT_VERSION, ubuntu_config in source.items():
        CUDA_NAME = meta[CUDA_TOOLKIT_VERSION]["package_name"]
        for UBUNTU_VERSION, python_config in ubuntu_config.items():
            for PYTHON_VERSION, torch_config in python_config.items():
                for TORCH_VERSION, image_states in torch_config.items():
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
