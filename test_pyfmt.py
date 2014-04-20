import baron
from pyfmt import format_code, find


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


def test_global():
    assert format_code("global     a") == "global a"


def test_while():
    assert format_code("while    a     :\n    pass") == "while a:\n    pass\n"


def test_for():
    assert format_code("for    a    in    b    :\n    pass") == "for a in b:\n    pass\n"


def test_if():
    assert format_code("if    a   :\n    pass") == "if a:\n    pass\n"


def test_elif():
    assert format_code("if    a   :\n    pass\nelif     b    :\n    pass\n") == "if a:\n    pass\nelif b:\n    pass\n"


def test_else():
    assert format_code("if    a   :\n    pass\nelse     :\n    pass\n") == "if a:\n    pass\nelse:\n    pass\n"


def test_lambda():
    assert format_code("lambda            :       a") == "lambda: a"
    assert format_code("lambda   a         :    a") == "lambda a: a"


def test_try():
    assert format_code("try     :\n    pass\nexcept:\n    pass\n") == "try:\n    pass\nexcept:\n    pass\n"


def test_except():
    assert format_code("try:\n    pass\nexcept     :\n    pass\n") == "try:\n    pass\nexcept:\n    pass\n"
    assert format_code("try:\n    pass\nexcept   a   :\n    pass\n") == "try:\n    pass\nexcept a:\n    pass\n"
    assert format_code("try:\n    pass\nexcept   a     ,    b  :\n    pass\n") == "try:\n    pass\nexcept a, b:\n    pass\n"
    assert format_code("try:\n    pass\nexcept   a     as    b  :\n    pass\n") == "try:\n    pass\nexcept a as b:\n    pass\n"


def test_finally():
    assert format_code("try:\n    pass\nfinally    :\n    pass\n") == "try:\n    pass\nfinally:\n    pass\n"


def test_dict():
    assert format_code("{       }") == "{}"
    assert format_code("{     a   :    b     }") == "{a: b}"
    assert format_code("{     a   :    b        ,   c   :    d     }") == "{a: b, c: d}"


def test_import():
    assert format_code("import           a") == "import a"
    assert format_code("import           a    ,      b      ,     d") == "import a, b, d"


def test_import_dot():
    assert format_code("import a  .  b  .  c") == "import a.b.c"


def test_from_import():
    assert format_code("from  .  a   import   b  , c") == "from .a import b, c"


def test_import_as():
    assert format_code("import a       as      b") == "import a as b"
    assert format_code("from c import a     as    b") == "from c import a as b"


def test_print():
    assert format_code("print    a") == "print a"
    assert format_code("print    >>    a   ,   b") == "print >>a, b"
    assert format_code("print    >>    a   ,   b  ,  c  ,  d") == "print >>a, b, c, d"


def test_find_endl_empty_string():
    assert find('endl', "") == None


def test_find_endl_dict_not_good():
    assert find('endl', {'type': 'pouet'}) == None


def test_find_endl_empty_list():
    assert find('endl', []) == None


def test_find_endl_list_not_good():
    assert find('endl', [{'type': 'pouet'}]) == None


def test_find_endl_dict_good():
    assert find('endl', {'type': 'endl'}) == {'type': 'endl'}


def test_find_endl_list_one():
    assert find('endl', [{'type': 'endl'}]) == {'type': 'endl'}


def test_find_endl_list_two():
    assert find('endl', [{'type': 'not_endl'}, {'type': 'endl'}]) == {'type': 'endl'}


def test_find_endl_first_one():
    assert find('endl', [{'type': 'endl', 'stuff': 'is_the_first'}, {'type': 'endl'}]) == {'type': 'endl', 'stuff': 'is_the_first'}


def test_find_endl_recursive():
    assert find('endl', {'type': 'pouet', 'stuff': {'type': 'endl'}}) == {'type': 'endl'}
    assert find('endl', {'type': 'pouet', 'stuff': [{'type': 'endl'}]}) == {'type': 'endl'}


def test_find_endl_functionnal():
    assert find('endl', baron.parse("[a, b, c]")[0]["value"]) == None
    assert find('endl', baron.parse("[a, b,\n c]")[0]["value"]) == {'formatting': [], 'indent': ' ', 'type': 'endl', 'value': '\n'}


def test_preserve_indent_in_list_in_root():
    assert format_code("[\n    a,\n    b,\n]") == "[\n    a,\n    b,\n]"


def test_preserve_indent_in_list_indented():
    assert format_code("if a:\n    a = [\n        a,\n        b,\n    ]") == "if a:\n    a = [\n        a,\n        b,\n    ]\n"


def test_preserve_indent_in_set_in_root():
    assert format_code("{\n    a,\n    b,\n}") == "{\n    a,\n    b,\n}"


def test_preserve_indent_in_set_indented():
    assert format_code("if a:\n    a = {\n        a,\n        b,\n    }") == "if a:\n    a = {\n        a,\n        b,\n    }\n"


def test_preserve_indent_in_dict_in_root():
    assert format_code("{\n    a,\n    b,\n}") == "{\n    a,\n    b,\n}"


def test_preserve_indent_in_dict_indented():
    assert format_code("if a:\n    a = {\n        a,\n        b,\n    }") == "if a:\n    a = {\n        a,\n        b,\n    }\n"


def test_preserve_indent_in_tuple_in_root():
    assert format_code("(\n    a,\n    b,\n)") == "(\n    a,\n    b,\n)"


def test_preserve_indent_in_tuple_indented():
    assert format_code("if a:\n    a = (\n        a,\n        b,\n    )") == "if a:\n    a = (\n        a,\n        b,\n    )\n"


nested_data_structure = """
a = [
    {
        a,
        b,
    },
]
"""

def test_nested_data_structure():
    assert format_code(nested_data_structure) == nested_data_structure


def test_not_keyword():
    assert format_code("not         a") == "not a"


def test_comment():
    assert format_code("#!/bin/bash") == "#!/bin/bash"
    assert format_code("#pouet") == "# pouet"
    assert format_code("##pouet") == "##pouet"
