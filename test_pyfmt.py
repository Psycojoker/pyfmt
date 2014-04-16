from pyfmt import format_code


def test_empty():
    assert format_code("") == ""
