#!/usr/bin/env python

import os
import sys
import argparse
import baron

def d(j):
    import json
    print json.dumps(j, indent=4)


dumpers = {}


def node(key=""):
    def wrap(func):
        if not key:
            dumpers[func.__name__ if not func.__name__.endswith("_") else func.__name__[:-1]] = func

        dumpers[key] = func
        return func
    return wrap


def find(node_type, tree):
    if isinstance(tree, dict):
        if tree["type"] == node_type:
            return tree
        for i in tree.values():
            result = find(node_type, i)
            if result is not None:
                return result
    elif isinstance(tree, list):
        for i in tree:
            result = find(node_type, i)
            if result is not None:
                return result
    return None


class Dumper(object):
    def __init__(self):
        self._current_indent = ""  # we always start at the level 0

    def dump_node(self, node):
        return "".join(list(dumpers[node["type"]](self, node)))


    def dump_node_list(self, node_list):
        return "".join(map(self.dump_node, node_list))


    @node()
    def endl(self, node):
        self._current_indent = node["indent"]
        yield self.dump_node_list(node["formatting"])
        yield node["value"]
        yield node["indent"]


    @node()
    def ternary_operator(self, node):
        yield self.dump_node(node["first"])
        yield " if "
        yield self.dump_node(node["value"])
        yield " else "
        yield self.dump_node(node["second"])


    @node("int")
    @node("name")
    @node("hexa")
    @node("octa")
    @node("float")
    @node("space")
    @node("binary")
    @node("complex")
    @node("float_exponant")
    @node("left_parenthesis")
    @node("right_parenthesis")
    def get_value(self, node):
        yield node["value"]


    @node("break")
    @node("continue")
    @node("pass")
    def get_type(self, node):
        yield node["type"]


    @node("star")
    @node("string")
    @node("raw_string")
    @node("binary_string")
    @node("unicode_string")
    @node("binary_raw_string")
    @node("unicode_raw_string")
    def generic(self, node):
        # TODO
        yield self.dump_node_list(node["first_formatting"])
        yield node["value"]
        yield self.dump_node_list(node["second_formatting"])


    @node()
    def comment(self, node):
        # FIXME ugly, comment can end up in formatting of another node or being
        # standalone, this is bad
        yield self.dump_node_list(node.get("formatting", []))
        yield node["value"]


    @node()
    def ellipsis(self, node):
        yield "..."


    @node()
    def dot(self, node):
        yield "."


    @node()
    def semicolon(self, node):
        # TODO I think that I should remove semicolon
        yield self.dump_node_list(node["first_formatting"])
        yield ";"
        yield self.dump_node_list(node["second_formatting"])


    @node()
    def comma(self, node):
        yield ", "


    @node()
    def call(self, node):
        yield "("
        yield self.dump_node_list(node["value"])
        yield ")"


    @node()
    def decorator(self, node):
        yield "@"
        yield self.dump_node(node["value"])
        if node["call"]:
            yield self.dump_node(node["call"])


    @node()
    def class_(self, node):
        yield self.dump_node_list(node["decorators"])
        yield "class "
        yield node["name"]
        if node["parenthesis"]:
            yield "("
        yield self.dump_node_list(node["inherit_from"])
        if node["parenthesis"]:
            yield ")"
        yield ":"
        yield self.dump_node_list(node["value"])


    @node()
    def repr(self, node):
        yield "`"
        yield self.dump_node_list(node["value"])
        yield "`"


    @node()
    def list_(self, node):
        yield "["
        if find('endl', node['value']):
            yield "".join(list(DataStructureDumper().dump_data_structure(node=node, indent=self._current_indent)))
        else:
            yield self.dump_node_list(node["value"])
        yield "]"


    @node()
    def associative_parenthesis(self, node):
        yield "("
        yield self.dump_node(node["value"])
        yield ")"


    @node()
    def tuple_(self, node):
        if node["with_parenthesis"]:
            yield "("
        yield self.dump_node_list(node["value"])
        if node["with_parenthesis"]:
            yield ")"


    @node()
    def funcdef(self, node):
        yield "def "
        yield node["name"]
        yield "("
        yield self.dump_node_list(node["arguments"])
        yield "):"
        yield self.dump_node_list(node["value"])


    @node()
    def call_argument(self, node):
        if node["name"]:
            yield node["name"]
            yield "="
            yield self.dump_node(node["value"])
        else:
            yield self.dump_node(node["value"])


    @node()
    def def_argument(self, node):
        if node["value"]:
            yield node["name"]
            yield "="
            yield self.dump_node(node["value"])
        elif isinstance(node["name"], basestring):
            yield node["name"]
        else:
            yield self.dump_node(node["name"])


    @node()
    def list_argument(self, node):
        yield "*"
        yield self.dump_node(node["value"])


    @node()
    def dict_argument(self, node):
        yield "**"
        yield self.dump_node(node["value"])


    @node()
    def return_(self, node):
        yield "return"
        if node["value"]:
            yield " "
            yield self.dump_node(node["value"])


    @node()
    def raise_(self, node):
        yield "raise"
        if node["value"]:
            yield " "
            yield self.dump_node(node["value"])
        if node["instance"]:
            yield ","
            yield " "
            yield self.dump_node(node["instance"])
        if node["traceback"]:
            yield ","
            yield " "
            yield self.dump_node(node["traceback"])


    @node()
    def assert_(self, node):
        yield "assert "
        yield self.dump_node(node["value"])
        if node["message"]:
            yield ", "
            yield self.dump_node(node["message"])


    @node("dotted_name")
    @node("ifelseblock")
    @node("atomtrailers")
    @node("string_chain")
    def dump_node_list_value(self, node):
        yield self.dump_node_list(node["value"])


    @node()
    def set_comprehension(self, node):
        yield "{"
        yield self.dump_node(node["result"])
        yield self.dump_node_list(node["generators"])
        yield "}"


    @node()
    def dict_comprehension(self, node):
        yield "{"
        yield self.dump_node(node["result"]["key"])
        yield ": "
        yield self.dump_node(node["result"]["value"])
        yield self.dump_node_list(node["generators"])
        yield "}"


    @node()
    def argument_generator_comprehension(self, node):
        yield self.dump_node(node["result"])
        yield self.dump_node_list(node["generators"])


    @node()
    def generator_comprehension(self, node):
        yield "("
        yield self.dump_node(node["result"])
        yield self.dump_node_list(node["generators"])
        yield ")"


    @node()
    def list_comprehension(self, node):
        yield "["
        yield self.dump_node(node["result"])
        yield self.dump_node_list(node["generators"])
        yield "]"


    @node()
    def comprehension_loop(self, node):
        "for x in x"
        yield " for "
        yield self.dump_node(node["iterator"])
        yield " in "
        if isinstance(node["target"], list):
            yield self.dump_node_list(node["target"])
        else:
            yield self.dump_node(node["target"])
        yield self.dump_node_list(node["ifs"])


    @node()
    def comprehension_if(self, node):
        yield " if "
        yield self.dump_node(node["value"])


    @node()
    def getitem(self, node):
        yield "["
        yield self.dump_node(node["value"])
        yield "]"


    @node()
    def slice(self, node):
        if node["lower"]:
            yield self.dump_node(node["lower"])
        yield self.dump_node_list(node["first_formatting"])
        yield ":"
        yield self.dump_node_list(node["second_formatting"])
        if node["upper"]:
            yield self.dump_node(node["upper"])

        if node["has_two_colons"]:
            yield self.dump_node_list(node["third_formatting"])
            yield ":"
            yield self.dump_node_list(node["fourth_formatting"])
            if node["step"]:
                yield self.dump_node(node["step"])


    @node()
    def assignment(self, node):
        yield self.dump_node(node["target"])
        yield " "
        if node.get("operator"):
            # FIXME should probably be a different node type
            yield node["operator"]
        yield "= "
        yield self.dump_node(node["value"])


    @node()
    def unitary_operator(self, node):
        yield node["value"]
        yield self.dump_node(node["target"])


    @node("binary_operator")
    @node("boolean_operator")
    @node("comparison")
    def binary_operator(self, node):
        yield self.dump_node(node["first"])
        yield " "
        if node["value"] == "not in": 
            yield "not in"
        else:
            yield node["value"]
        yield " "
        yield self.dump_node(node["second"])


    @node()
    def with_(self, node):
        yield "with "
        yield self.dump_node_list(node["contexts"])
        yield ":"
        yield self.dump_node_list(node["value"])


    @node()
    def with_context_item(self, node):
        yield self.dump_node(node["value"])
        if node["as"]:
            yield " as "
            yield self.dump_node(node["as"])


    @node()
    def del_(self, node):
        yield "del "
        yield self.dump_node(node["value"])


    @node()
    def yield_(self, node):
        yield "yield"
        if node["value"]:
            yield " "
            yield self.dump_node(node["value"])


    @node()
    def yield_atom(self, node):
        yield "(yield "
        if node["value"]:
            yield self.dump_node(node["value"])
        yield ")"


    @node()
    def exec_(self, node):
        yield "exec "
        yield self.dump_node(node["value"])
        if node["globals"]:
            yield " in "
            yield self.dump_node(node["globals"])
        if node["locals"]:
            yield ", "
            yield self.dump_node(node["locals"])


    @node()
    def global_(self, node):
        yield "global "
        yield self.dump_node_list(node["value"])


    @node()
    def while_(self, node):
        yield "while "
        yield self.dump_node(node["test"])
        yield ":"
        yield self.dump_node_list(node["value"])
        if node["else"]:
            yield self.dump_node(node["else"])


    @node()
    def for_(self, node):
        yield "for "
        yield self.dump_node(node["iterator"])
        yield " in "
        yield self.dump_node(node["target"])
        yield ":"
        yield self.dump_node_list(node["value"])
        if node["else"]:
            yield self.dump_node(node["else"])


    @node()
    def if_(self, node):
        yield "if "
        yield self.dump_node(node["test"])
        yield ":"
        yield self.dump_node_list(node["value"])


    @node()
    def elif_(self, node):
        yield "elif "
        yield self.dump_node(node["test"])
        yield ":"
        yield self.dump_node_list(node["value"])


    @node()
    def else_(self, node):
        yield "else:"
        yield self.dump_node_list(node["value"])


    @node()
    def lambda_(self, node):
        yield "lambda"
        if node["arguments"]:
            yield " "
            yield self.dump_node_list(node["arguments"])
        yield ": "
        yield self.dump_node(node["value"])


    @node()
    def try_(self, node):
        yield "try:"
        yield self.dump_node_list(node["value"])
        yield self.dump_node_list(node["excepts"])
        if node["else"]:
            yield self.dump_node(node["else"])
        if node["finally"]:
            yield self.dump_node(node["finally"])


    @node()
    def except_(self, node):
        yield "except"
        if node["exception"]:
            yield " "
            yield self.dump_node(node["exception"])
        if node["delimiteur"]:
            if node["delimiteur"] == "as":
                yield " "
            yield node["delimiteur"]
            yield " "
            yield self.dump_node(node["target"])
        yield ":"
        yield self.dump_node_list(node["value"])


    @node()
    def finally_(self, node):
        yield "finally:"
        yield self.dump_node_list(node["value"])


    @node("dict")
    @node("set")
    def dict_or_set(self, node):
        yield "{"
        yield self.dump_node_list(node["value"])
        yield "}"


    @node()
    def dictitem(self, node):
        yield self.dump_node(node["key"])
        yield ": "
        yield self.dump_node(node["value"])


    @node()
    def import_(self, node):
        yield "import "
        yield self.dump_node_list(node["value"])


    @node()
    def from_import(self, node):
        yield "from "
        yield self.dump_node(node["value"])
        yield " import "
        yield self.dump_node_list(node["targets"])


    @node()
    def dotted_as_name(self, node):
        yield self.dump_node_list(node["value"]["value"])
        if node["as"]:
            yield " as "
            yield node["target"]


    @node()
    def name_as_name(self, node):
        yield node["value"]
        if node["as"]:
            yield " as "
            yield node["target"]


    @node()
    def print_(self, node):
        yield "print"
        if node["destination"]:
            yield " >>"
            yield self.dump_node(node["destination"])
        if node["value"]:
            if node["value"][0]["type"] != "comma":
                yield " "
            yield self.dump_node_list(node["value"])


    def dumps(self, tree):
        return "".join(map(self.dump_node, tree))


class DataStructureDumper(Dumper):
    def dump_data_structure(self, node, indent):
        yield "\n    " + indent
        to_yield = ""
        for i in node["value"]:
            if i["type"] != "comma":
                to_yield += self.dump_node(i)
            else:
                to_yield += ",\n    " + indent
        to_yield = to_yield.rstrip()
        yield to_yield
        yield "\n" + indent


def format_code(source_code):
    return Dumper().dumps(baron.parse(source_code))


def main():
    parser = argparse.ArgumentParser(description='Auto format a python file following the pep8 convention.')
    parser.add_argument('file_name', metavar='file_name', type=str, help='file name')
    parser.add_argument('-i', dest='in_place', action='store_true', default=False, help='in place modification, like sed')

    args = parser.parse_args()
    if not os.path.exists(args.file_name):
        sys.stderr.write("Error: the file '%s' does not exist.\n" % args.file_name)
        sys.exit(1)

    sys.stdout.write(format_code(open(args.file_name, "r").read()))


if __name__ == '__main__':
    main()
