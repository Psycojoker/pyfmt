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


def test_class_simple():
    assert format_code("class     A :\n    pass") == "class A:\n    pass\n"
    assert format_code("class     A  (   ) :\n    pass") == "class A():\n    pass\n"
    assert format_code("class     A  ( zob  ) :\n    pass") == "class A(zob):\n    pass\n"
    assert format_code("class     A  ( zob    , plop  ) :\n    pass") == "class A(zob, plop):\n    pass\n"


def test_repr():
    assert format_code("`   a  `") == "`a`"


def test_list():
    assert format_code("[ a  ,    b  ,    c    ]") == "[a, b, c]"


def test_associative_parenthesis():
    assert format_code("(    b  )") == "(b)"


def test_tuple():
    assert format_code("a   ,  b") == "a, b"
    assert format_code("(  a   ,  b     )") == "(a, b)"


def test_funcdef():
    assert format_code("def  a   (    )   :\n    pass") == "def a():\n    pass\n"


def test_call_argument():
    assert format_code("a(  b   =      c )") == "a(b=c)"


def test_def_arguments():
    assert format_code("def a(   b       =False):\n    pass") == "def a(b=False):\n    pass\n"


def test_def_arguments_list_argument():
    assert format_code("def a(  * b  ):\n    pass") == "def a(*b):\n    pass\n"


def test_def_arguments_dict_argument():
    assert format_code("def a(  ** b  ):\n    pass") == "def a(**b):\n    pass\n"


def test_return():
    assert format_code("return") == "return"
    assert format_code("return     a") == "return a"
