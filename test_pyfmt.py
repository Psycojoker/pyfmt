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
    assert format_code("`   a  `") == "repr(a)"


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


def test_decorator():
    assert format_code("@a\ndef a():\n    pass") == "@a\ndef a():\n    pass\n"
    assert format_code("@a\nclass a():\n    pass") == "@a\nclass a():\n    pass\n"


def test_string_formatting_special_case():
    assert format_code("'a' + 1") == "'a' + 1"
    assert format_code("'a'\n'b'") == "'a'\n'b'"


def test_before_comment_formatting():
    assert format_code("a # b") == "a  # b"


def test_comment_not_empty_line():
    assert format_code("'1' # b") == "'1'  # b"


def test_comment_empty_line():
    assert format_code("# b") == "# b"


def test_comment_after_colon_statement():
    assert format_code("try:# pouet\n    pass\nexcept:\n    pass\n") == "try:  # pouet\n    pass\nexcept:\n    pass\n"


def test_comment_empty_line_indented():
    assert format_code("if a:\n    # pouet\n    pass\n") == "if a:\n    # pouet\n    pass\n"


def test_add_endl_one_line_suite_if():
    assert format_code("if a: pass") == "if a:\n    pass\n"


def test_add_endl_one_line_suite_elif():
    assert format_code("if a:\n    pass\nelif a: pass") == "if a:\n    pass\nelif a:\n    pass\n"


def test_add_endl_one_line_suite_else():
    assert format_code("if a:\n    pass\nelse: pass") == "if a:\n    pass\nelse:\n    pass\n"


def test_add_endl_one_line_suite_for():
    assert format_code("for a in a: pass") == "for a in a:\n    pass\n"


def test_add_endl_one_line_suite_try():
    assert format_code("try: pass\nexcept:\n    pass\n") == "try:\n    pass\nexcept:\n    pass\n"


def test_add_endl_one_line_suite_except():
    assert format_code("try:\n    pass\nexcept: pass\n") == "try:\n    pass\nexcept:\n    pass\n"


def test_add_endl_one_line_suite_finally():
    assert format_code("try:\n    pass\nfinally: pass\n") == "try:\n    pass\nfinally:\n    pass\n"


def test_add_endl_one_line_suite_with():
    assert format_code("with a: pass") == "with a:\n    pass\n"


def test_add_endl_one_line_suite_class():
    assert format_code("class a: pass") == "class a:\n    pass\n"


def test_add_endl_one_line_suite_while():
    assert format_code("while a: pass") == "while a:\n    pass\n"


def test_add_endl_one_line_suite_funcdef():
    assert format_code("def a(): pass") == "def a():\n    pass\n"


def test_replace_repr_by_function_call():
    assert format_code("`a`") == "repr(a)"


one_line_import = "import a, b.e.f, c as pouet, d.d as i"
split_import = """\
import a
import b.e.f
import c as pouet
import d.d as i"""


one_line_import_indented = "if a:\n    import a, b.e.f, c as pouet, d.d as i"
split_import_indented = """\
if a:
    import a
    import b.e.f
    import c as pouet
    import d.d as i
"""


def test_split_import():
    assert format_code(one_line_import) == split_import


def test_split_import_indented():
    assert format_code(one_line_import_indented) == split_import_indented


comment_2_spaces_target = """\
class A:# stuff
    def a():# stuff
        try:# stuff
            pass
        except:# stuff
            pass
        finally:# stuff
            pass
        for a in a:# stuff
            pass
"""


comment_2_spaces_target_result = """\
class A:  # stuff
    def a():  # stuff
        try:  # stuff
            pass
        except:  # stuff
            pass
        finally:  # stuff
            pass
        for a in a:  # stuff
            pass
"""


def test_comment_indented_after_try():
    assert format_code(comment_2_spaces_target) == comment_2_spaces_target_result


def test_tuple_trailing():
    assert format_code("(3,)") == "(3,)"


def test_list_trailing():
    assert format_code("[3,]") == "[3,]"


def test_set_trailing():
    assert format_code("{3,}") == "{3,}"


def test_dict_trailing():
    assert format_code("{3: 3,}") == "{3: 3,}"


def test_empty_comment_no_space():
    assert format_code("#") == "#"


def test_simily_print_function_stuff():
    assert format_code("print(a)") == "print(a)"


def test_replace_tabs():
    assert format_code("if a:\n    if b:\n	pass\n\n") == "if a:\n    if b:\n        pass\n\n"

bad_indentation = """\
if a:
 if b:
  if c:
   if d:
    pouet
  plop
 pop
"""

bad_indentation_fixed = """\
if a:
    if b:
        if c:
            if d:
                pouet
        plop
    pop
"""


def test_fix_bad_indentation_simple_too_small():
    assert format_code("if a:\n pass") == "if a:\n    pass\n"


def test_fix_bad_indentation_simple_too_big():
    assert format_code("if a:\n            pass") == "if a:\n    pass\n"


def test_fix_indentation_complex():
    print("result:")
    print(format_code(bad_indentation))
    print("expected:")
    print(bad_indentation_fixed)
    assert format_code(bad_indentation) == bad_indentation_fixed

bug_reindent_tabs = """
if b:
	if a:
		pass
		pass
		pass
"""

bug_reindent_tabs_fixed = """
if b:
    if a:
        pass
        pass
        pass
"""


def test_bug_reindent_tabs():
    assert format_code(bug_reindent_tabs) == bug_reindent_tabs_fixed


root_level_function = """
pouet
import a
def plop():
    pass
plop
pop
"""


root_level_function_fixed = """
pouet
import a


def plop():
    pass


plop
pop
"""


def test_blank_lines_arround_functions_first_level():
    assert format_code(root_level_function) == root_level_function_fixed


def test_blank_lines_arround_class_first_level():
    assert format_code(root_level_function.replace('def', 'class')) == root_level_function_fixed.replace('def', 'class')


def test_replace_windows_endl():
    assert format_code("\r\n") == "\n"


class_level_function = """\
class A:
    def plop():
        pass
    def pop():
        pass
    def ploup():
        pass
"""


class_level_function_fixed = """\
class A:
    def plop():
        pass

    def pop():
        pass

    def ploup():
        pass
"""


def test_blank_lines_arround_methods():
    assert format_code(class_level_function) == class_level_function_fixed


def test_split_semicolon():
    assert format_code("a;b") == "a\nb"


def test_split_semicolon_indented():
    assert format_code("\n    a;b") == "\n    a\n    b"


def test_replace_old_comparison_operator():
    assert format_code("a <> b") == "a != b"


comment_previous_endl_indent = """\
class A:
    a = b
    # should not be indented
    b = c
"""


def test_comment_previous_endl_indent_regression_test():
    assert format_code(comment_previous_endl_indent) == comment_previous_endl_indent


def test_respect_backslash():
    respect_backslash = "a ==\\\n  b"
    assert format_code(respect_backslash) == respect_backslash
    respect_backslash = "a \\\n== b"
    assert format_code(respect_backslash) == respect_backslash


# Disable test because the many line statement is a big subject
# def test_on_Self():
#    assert format_code(open("./pyfmt.py", "r").read()) == open("./pyfmt.py", "r").read()


def test_on_self_tests():
    assert format_code(open("./test_pyfmt.py", "r").read()) == open("./test_pyfmt.py", "r").read()
