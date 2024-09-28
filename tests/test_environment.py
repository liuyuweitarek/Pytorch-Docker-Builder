import pytest

def test_import_torch_success(torch_module):
    assert torch_module is not None

def test_cuda_available(torch_module):
    assert torch_module.cuda.is_available()

