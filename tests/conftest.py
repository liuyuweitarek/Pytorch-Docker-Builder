import pytest

@pytest.fixture(scope="session")
def compatible_source_file_path() -> str:
    return "config/compatible_versions_source.json"

@pytest.fixture(scope="session")
def compatible_target_file_path() -> str:
    return "config/compatible_versions_target.json"

@pytest.fixture(scope="module")
def torch_module():
    try:
        import torch
        return torch
    except ModuleNotFoundError:
        raise ModuleNotFoundError("No module named \'torch\'")
