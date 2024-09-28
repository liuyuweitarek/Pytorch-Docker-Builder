import json
from typing import Union, Optional

from constants import COMPATIBLE_SOURCE_FILE, COMPATIBLE_TARGET_FILE


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


def update_compatible_version(
    source_file: str = COMPATIBLE_SOURCE_FILE,
    updated_file: str = COMPATIBLE_TARGET_FILE,
) -> None:

    compatible_versions: List[Dict[str, str]] = []

    source = read_json(source_file)

    for CUDA_TOOLKIT_VERSION, config in source.items():

        CUDA_NAME = config["package_name"]

        for UBUNTU_VERSION in config["ubuntu_avaiable"]:
            for PYTHON_VERSION, available_torch_version in config[
                "python_available_torch"
            ].items():
                for TORCH_VERSION in available_torch_version:
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

    write_json(data=compatible_versions, filename=updated_file)
