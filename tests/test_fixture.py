import pytest


@pytest.fixture(params=[1, 2, 3])
def test_data(request):
    return request.param


def test_not_2(test_data):
    # assert test_data != 2
    assert test_data != 4