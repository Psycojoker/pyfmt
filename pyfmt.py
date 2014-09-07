#!/usr/bin/env python

import os
import re
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
            dumpers[func.__name__ if not func.__name__.endswith(
                "_") else func.__name__[:-1]] = func

        dumpers[key] = func
        return func
    return wrap


def find(node_type, tree):
    if isinstance(tree, dict):
        if tree.get("type") == node_type:
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
        self.previous = None
        self.stack = []
        self.indentation_stack = []
        self.number_of_endl = 0

    def maybe_backslash(self, formatting, default):
        if formatting and "\\" in formatting[0]["value"]:
            return formatting[0]["value"]
        else:
            return default

    def dump_node(self, node):
        self.stack.append(node)
        if node["type"] == "endl":
            self.number_of_endl += 1
        elif node["type"] not in ('space', 'comment'):
            self.number_of_endl = 0
        to_return = "".join(list(dumpers[node["type"]](self, node)))
        self.stack.pop()
        return to_return

    def dump_node_list(self, node_list):
        to_return = ""
        for node in node_list:
            to_return += self.dump_node(node)
            self.previous = node
        return to_return

    def dump_root(self, node_list):
        to_return = ""
        previous_is_function = False
        for statement_number, node in enumerate(node_list):
            if node["type"] not in ('endl', 'comment', 'space'):
                if node["type"] in ("funcdef", "class") and self.number_of_endl != 3 and statement_number != 0:
                    to_return += "\n" * (3 - self.number_of_endl)
                    previous_is_function = True
                elif previous_is_function:
                    previous_is_function = False
                    to_return += "\n" * (3 - self.number_of_endl)

            to_return += self.dump_node(node)
            self.previous = node
        return to_return

    def dump_suite(self, node_list):
        if node_list and node_list[0]["type"] != "endl":
            node_list = [
                {"type": "endl", "formatting": [], "value": "\n", "indent": self._current_indent + "    "}] + node_list
        return self.dump_node_list(node_list)

    def dump_class_body(self, node_list):
        if node_list and node_list[0]["type"] != "endl":
            node_list = [
                {"type": "endl", "formatting": [], "value": "\n", "indent": self._current_indent + "    "}] + node_list

        to_return = ""
        previous_is_function = False
        for statement_number, node in enumerate(node_list):
            if node["type"] not in ('endl', 'comment', 'space'):
                if node["type"] == "funcdef" and self.number_of_endl != 3 and statement_number != 1:
                    to_return = re.sub(' *$', '', to_return)
                    to_return += "\n" * \
                        (2 - self.number_of_endl) + self._current_indent
                    previous_is_function = True
                elif previous_is_function:
                    previous_is_function = False
                    to_return += "\n" * (2 - self.number_of_endl)
            to_return += self.dump_node(node)
            self.previous = node
        return to_return

    @node()
    def endl(self, node):
        # replace tab with space
        indentation = node["indent"].replace("\t", " " * 8)

        # reindentation rules
        # self.indentation_stack store tuples ('found intentation', 'correct
        # indentation')
        if len(indentation) == 0:
            pass

        elif len(self.indentation_stack) == 0:
            if len(indentation) != 4:
                self.indentation_stack.append((indentation, " " * 4))
                indentation = " " * 4
            else:
                self.indentation_stack.append((indentation, indentation))

        elif indentation > self.indentation_stack[-1][0]:
            if indentation != self.indentation_stack[-1][1] + " " * 4:
                self.indentation_stack.append(
                    (indentation, self.indentation_stack[-1][1] + " " * 4))
                indentation = self.indentation_stack[-2][1] + " " * 4
            else:
                self.indentation_stack.append((indentation, indentation))

        elif indentation < self.indentation_stack[-1][0]:
            while self.indentation_stack and indentation != self.indentation_stack[-1][0]:
                self.indentation_stack.pop()
            if not self.indentation_stack:
                self.indentation = ""
            elif indentation != self.indentation_stack[-1][1]:
                indentation = self.indentation_stack[-1][1]

        elif indentation == self.indentation_stack[-1][0]:
            indentation = self.indentation_stack[-1][1]

        self._current_indent = indentation
        yield self.dump_node_list(node["formatting"])
        yield "\n"
        yield indentation

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
        if find('endl', node["first_formatting"]):
            yield self.dump_node_list(node["first_formatting"])
        yield node["value"]
        if find('endl', node["second_formatting"]):
            yield self.dump_node_list(node["second_formatting"])

    @node()
    def comment(self, node):
        if self.previous and self.previous["type"] != "endl":
            yield "  "
        if node["value"].startswith(("# ", "##", "#!")) or len(node["value"]) == 1:
            yield node["value"]
        else:
            yield "# " + node["value"][1:]

    @node()
    def ellipsis(self, node):
        yield "..."

    @node()
    def dot(self, node):
        yield "."

    @node()
    def semicolon(self, node):
        yield "\n" + self._current_indent

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
        self.previous = node
        yield self.dump_class_body(node["value"])

    @node()
    def repr(self, node):
        yield "repr("
        yield self.dump_node_list(node["value"])
        yield ")"

    @node()
    def list_(self, node):
        yield "["
        yield self._dump_data_structure_body(node)
        yield "]"

    def _dump_data_structure_body(self, node):
        if find('endl', node['value']):
            return "".join(list(self.dump_data_structure(content=node["value"],
                                                         indent=self._current_indent)))
        else:
            return re.sub("([^\n ]) +$", "\g<1>", self.dump_node_list(node["value"]))

    @node()
    def associative_parenthesis(self, node):
        yield "("
        yield self.dump_node(node["value"])
        yield ")"

    @node()
    def tuple_(self, node):
        if node["with_parenthesis"]:
            yield "("
        yield self._dump_data_structure_body(node)
        if node["with_parenthesis"]:
            yield ")"

    @node()
    def funcdef(self, node):
        yield self.dump_node_list(node["decorators"])
        yield "def "
        yield node["name"]
        yield "("
        yield self.dump_node_list(node["arguments"])
        yield "):"
        self.previous = node
        yield self.dump_suite(node["value"])

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
        if node["value"] == "not":
            yield " "
        yield self.dump_node(node["target"])

    @node("binary_operator")
    @node("boolean_operator")
    @node("comparison")  # XXX comparison will need a new function in the futur
    def binary_operator(self, node):
        yield self.dump_node(node["first"])
        yield self.maybe_backslash(node["first_formatting"], " ")
        if isinstance(node["value"], basestring):
            if node["value"] == "not in":
                yield "not in"
            elif node["value"] == "is not":
                yield "is not"
            else:
                yield node["value"].replace("<>", "!=")
        else:
            yield self.dump_node(node["value"])
        yield self.maybe_backslash(node["second_formatting"], " ")
        yield self.dump_node(node["second"])

    @node()
    def complex_operator(self, node):
        yield node["first"]
        yield self.maybe_backslash(node["formatting"], " ")
        yield node["second"]

    @node()
    def with_(self, node):
        yield "with "
        yield self.dump_node_list(node["contexts"])
        yield ":"
        self.previous = node
        yield self.dump_suite(node["value"])

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
        self.previous = node
        yield self.dump_suite(node["value"])
        if node["else"]:
            yield self.dump_node(node["else"])

    @node()
    def for_(self, node):
        yield "for "
        yield self.dump_node(node["iterator"])
        yield " in "
        yield self.dump_node(node["target"])
        yield ":"
        self.previous = node
        yield self.dump_suite(node["value"])
        if node["else"]:
            yield self.dump_node(node["else"])

    @node()
    def if_(self, node):
        yield "if "
        yield self.dump_node(node["test"])
        yield ":"
        self.previous = node
        yield self.dump_suite(node["value"])

    @node()
    def elif_(self, node):
        yield "elif "
        yield self.dump_node(node["test"])
        yield ":"
        self.previous = node
        yield self.dump_suite(node["value"])

    @node()
    def else_(self, node):
        yield "else:"
        self.previous = node
        yield self.dump_suite(node["value"])

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
        self.previous = node
        yield self.dump_suite(node["value"])
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
        if node["delimiter"]:
            if node["delimiter"] == "as":
                yield " "
            yield node["delimiter"]
            yield " "
            yield self.dump_node(node["target"])
        yield ":"
        self.previous = node
        yield self.dump_suite(node["value"])

    @node()
    def finally_(self, node):
        yield "finally:"
        self.previous = node
        yield self.dump_suite(node["value"])

    @node("dict")
    @node("set")
    def dict_or_set(self, node):
        yield "{"
        yield self._dump_data_structure_body(node)
        yield "}"

    @node()
    def dictitem(self, node):
        yield self.dump_node(node["key"])
        yield ": "
        yield self.dump_node(node["value"])

    @node()
    def import_(self, node):
        to_yield = []
        for i in filter(lambda x: x["type"] != "comma", node["value"]):
            to_yield.append("import " + self.dump_node(i))
        yield ("\n" + self._current_indent).join(to_yield)

    @node()
    def from_import(self, node):
        yield "from "
        yield self.dump_node_list(node["value"])
        yield " import "
        yield self.dump_node_list(node["targets"])

    @node()
    def dotted_as_name(self, node):
        yield self.dump_node_list(node["value"])
        if node["target"]:
            yield " as "
            yield node["target"]

    @node()
    def name_as_name(self, node):
        yield node["value"]
        if node["target"]:
            yield " as "
            yield node["target"]

    @node()
    def print_(self, node):
        yield "print"
        if node["destination"]:
            yield " >>"
            yield self.dump_node(node["destination"])
        if node["value"]:
            to_yield = self.dump_node_list(node["value"])
            if to_yield.startswith("(") and to_yield.endswith(")") and "," not in to_yield:
                pass
            elif node["value"][0]["type"] != "comma":
                yield " "
            yield to_yield

    dumps = dump_node_list

    def dump_data_structure(self, content, indent):
        yield "\n    " + indent
        to_yield = ""
        self._current_indent = indent + "    "
        for i in content:
            if i["type"] != "comma":
                to_yield += self.dump_node(i)
            else:
                to_yield += ",\n    " + indent
        to_yield = to_yield.rstrip()
        yield to_yield
        yield "\n" + indent
        self._current_indent = self._current_indent[:-4]


def format_code(source_code):
    return Dumper().dump_root(baron.parse(source_code))


def main():
    parser = argparse.ArgumentParser(
        description='Auto format a python file following the pep8 convention.')
    parser.add_argument(
        'file_name', metavar='file_name', type=str, help='file name')
    parser.add_argument('-i', dest='in_place', action='store_true',
                        default=False, help='in place modification, like sed')

    args = parser.parse_args()
    if not os.path.exists(args.file_name):
        sys.stderr.write(
            "Error: the file '%s' does not exist.\n" % args.file_name)
        sys.exit(1)

    if not args.in_place:
        sys.stdout.write(format_code(open(args.file_name, "r").read()))
    else:
        result = format_code(open(args.file_name, "r").read())
        open(args.file_name, "w").write(result)


if __name__ == '__main__':
    main()
