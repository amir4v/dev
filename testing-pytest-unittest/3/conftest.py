import pytest


@pytest.fixture
def get_tuple():
    return ((1,2), (2,1))
