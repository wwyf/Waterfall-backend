import pytest

params = [
    (2, 3, 5),
    (4, 5, 9),
    (6, 7, 13)
]


@pytest.mark.parametrize('a, b, expected', params)
def test_add(a, b, expected):
    assert a + b == expected