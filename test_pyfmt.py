from pyfmt import format_code


def test_empty():
    assert format_code("") == ""


def test_ternary_operator():
    assert format_code("a  if   b     	 else        c") == "a if b else c"


def test_ellipsis():
    assert format_code("a[.  .    .]") == "a[...]"


def test_dot():
    assert format_code("a .    b") == "a.b"


def test_comma():
    assert format_code("a   ,     c") == "a, c"


def test_call():
    assert format_code("a  (    b    	)") == "a(b)"
