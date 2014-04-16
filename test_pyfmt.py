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


def test_raise():
    assert format_code("raise      Exception()") == "raise Exception()"
    assert format_code("raise      Exception()  ,     b") == "raise Exception(), b"
    assert format_code("raise      Exception()  ,     b    ,     c") == "raise Exception(), b, c"


def test_assert():
    assert format_code("assert    a") == "assert a"
    assert format_code("assert    a         ,   b") == "assert a, b"


def test_set_comprehension():
    assert format_code("{  x      for  x     in     x   }") == "{x for x in x}"


def test_dict_comprehension():
    assert format_code("{  x    :  z      for  x     in     x   }") == "{x: z for x in x}"


def test_generator_comprehension():
    assert format_code("(  x      for  x     in     x   )") == "(x for x in x)"


def test_list_comprehension():
    assert format_code("[  x      for  x     in     x   ]") == "[x for x in x]"


def test_if_comprehension():
    assert format_code("[  x      for  x     in     x      if      x]") == "[x for x in x if x]"


def test_getitem():
    assert format_code("a[  b  ]") == "a[b]"


def test_assignement():
    assert format_code("a     =        b") == "a = b"


def test_augassign():
    assert format_code("a     +=    b") == "a += b"


def test_unitary_operator():
    assert format_code("-   a") == "-a"


def test_binary_operator():
    assert format_code("a     +                  b") == "a + b"


def test_comparison():
    assert format_code("a   >     b") == "a > b"


def test_boolean_operator():
    assert format_code("a     and        b") == "a and b"


def test_not_in():
    assert format_code("a     not    in      b") == "a not in b"


def test_with():
    assert format_code("with     a     :\n    pass") == "with a:\n    pass\n"


def test_with_as():
    assert format_code("with     a     as   b    :\n    pass") == "with a as b:\n    pass\n"


def test_del():
    assert format_code("del     a") == "del a"


def test_yield():
    assert format_code("yield") == "yield"
    assert format_code("yield            a") == "yield a"


def test_yield_atom():
    assert format_code("a = (        yield     a    )") == "a = (yield a)"


def test_exec():
    assert format_code("exec     a") == "exec a"
    assert format_code("exec     a         in       b") == "exec a in b"
    assert format_code("exec     a         in       b       ,      c") == "exec a in b, c"
