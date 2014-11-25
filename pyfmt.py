#!/usr/bin/env python

import os
import re
import sys
import argparse
import logging

import baron


python_version = sys.version_info[0]
python_subversion = sys.version_info[1]
string_instance = str if python_version == 3 else basestring


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


def format_code(source_code):
    result = ""
    state = {
        "previous": None,
        "current_indent": "",
        "number_of_endl": 0,
        "indentation_stack": [],
    }

    previous_is_function = False
    for statement_number, node in enumerate(baron.parse(source_code)):
        if node["type"] not in ('endl', 'comment', 'space'):
            if node["type"] in ("def", "class") and state["number_of_endl"] != 3 and statement_number != 0:
                result += "\n"*(3 - state["number_of_endl"])
                previous_is_function = True
            elif previous_is_function:
                previous_is_function = False
                result += "\n" * (3 - state["number_of_endl"])

        result += _generator_to_string(_render_node(node, state))
        state["previous"] = node

    return result


def _generator_to_string(generator):
    return "".join(list(generator))


def _render_list(node_type, key_name, nodes_list, state):
    if custom_key_renderers.get(node_type, {}).get(key_name) is None:
        for node in nodes_list:
            yield _generator_to_string(_render_node(node, state))

    else:
        for i in custom_key_renderers[node_type][key_name](node_type, key_name, nodes_list, state):
            yield i


def _render_node(node, state):
    node_rendering_order = baron.nodes_rendering_order[node["type"]]

    for key_type, key_name, display_condition in node_rendering_order:
        for_debug = "%s %s %s %s %s " % (node["type"], key_name, key_type, [node.get(key_name)], "----->",)

        if node["type"] == "endl":
            state["number_of_endl"] += 1
        else:
            state["number_of_endl"] = 0

        if node["type"] in advanced_formatters:
            logging.debug(for_debug + "advanced formatters")
            yield advanced_formatters[node["type"]](node, state)
            break

        if display_condition is False or (display_condition is not True and not node[display_condition]):
            logging.debug(for_debug + "not displayed")
            state["previous"] = node
            continue

        if key_type == "constant":
            logging.debug(for_debug + "constant")
            yield key_name
        elif key_type == "formatting":
            logging.debug(for_debug + "formatting")
            state["previous"] = node
            yield _render_key(node["type"], key_name, " ", node, state)
        elif key_type == "string":
            logging.debug(for_debug + "string")
            yield node[key_name]
        elif key_type == "key":
            logging.debug(for_debug + "key")
            state["previous"] = node
            yield _generator_to_string(_render_node(node[key_name], state))
        elif key_type == "list":
            logging.debug(for_debug + "list")
            state["previous"] = node
            yield _generator_to_string(_render_list(node["type"], key_name, node[key_name], state))
        elif key_type == "bool":
            logging.debug(for_debug + "bool")
            pass
        else:
            raise Exception("Unhandled key type: %s" % key_type)

    logging.debug("%s %s" % ("set as previous", node["type"]))
    state["previous"] = node


def dont_break_backslash(to_test, normal_value, key_name=None):
    logging.debug("%s %s %s %s" % ("don't break backslash", [to_test], [normal_value], key_name))
    if isinstance(to_test, list):
        to_test = _generator_to_string(_render_list(None, None, to_test, {}))

    if key_name is not None and "formatting" not in key_name:
        return normal_value

    if "\\" in to_test:
        return to_test

    return normal_value


def _render_key(node_type, key_name, value, node, state):
    if custom_key_renderers.get(node_type, {}).get(key_name) is None:
        return dont_break_backslash(to_test=node[key_name], normal_value=value, key_name=key_name)

    return custom_key_renderers[node_type][key_name](value, key_name, node, state)


empty_string = lambda value, key_name, node, state: dont_break_backslash(to_test=node[key_name], normal_value="", key_name=key_name)


def suite(node_type, key_name, node_list, state):
    if node_list and node_list[0]["type"] != "endl":
        node_list = [
            {"type": "endl", "formatting": [], "value": "\n", "indent": state["current_indent"] + "    "}] + node_list
    return _render_list(None, None, node_list, state)


def dump_data_structure_body(node_type, key_name, node_list, state):
    if not find('endl', node_list):
        return re.sub("([^\n ]) +$", "\g<1>", _generator_to_string(_render_list(None, None, node_list, state)))

    to_return = "\n    " + state["current_indent"]
    state["current_indent"] += "    "

    for i in node_list:
        if i["type"] != "comma":
            to_return += _generator_to_string(_render_node(i, state))
        else:
            to_return += ",\n" + state["current_indent"]

    to_return = to_return.rstrip()
    state["current_indent"] = state["current_indent"][:-4]
    to_return += "\n" + state["current_indent"]

    return to_return


custom_key_renderers = {
    "assert": {
        "second_formatting": empty_string,
    },
    "associative_parenthesis": {
        "first_formatting": empty_string,
        "second_formatting": empty_string,
        "third_formatting": empty_string,
        "fourth_formatting": empty_string,
    },
    "call": {
        "first_formatting": empty_string,
        "second_formatting": empty_string,
        "third_formatting": empty_string,
        "fourth_formatting": empty_string,
    },
    "call_argument": {
        "first_formatting": empty_string,
        "second_formatting": empty_string,
    },
    "class": {
        "value": suite,
        "second_formatting": empty_string,
        "third_formatting": empty_string,
        "fourth_formatting": empty_string,
        "fifth_formatting": empty_string,
        "sixth_formatting": empty_string,
    },
    "comma": {
        "first_formatting": empty_string,
    },
    "comparison_operator": {
        "formatting": lambda value, key_name, node, state: dont_break_backslash(to_test=node[key_name], normal_value=" " if node["second"] else ""),
    },
    "def": {
        "value": suite,
        "second_formatting": empty_string,
        "third_formatting": empty_string,
        "fourth_formatting": empty_string,
        "fifth_formatting": empty_string,
        "sixth_formatting": empty_string,
    },
    "def_argument": {
        "first_formatting": empty_string,
        "second_formatting": empty_string,
    },
    "dict": {
        "value": dump_data_structure_body,
        "first_formatting": empty_string,
        "second_formatting": empty_string,
        "third_formatting": empty_string,
        "fourth_formatting": empty_string,
    },
    "dictitem": {
        "first_formatting": empty_string,
    },
    "dict_argument": {
        "formatting": empty_string,
    },
    "dict_comprehension": {
        "first_formatting": empty_string,
        "second_formatting": empty_string,
        "third_formatting": empty_string,
        "fourth_formatting": empty_string,
    },
    "dot": {
        "first_formatting": empty_string,
        "second_formatting": empty_string,
    },
    "elif": {
        "value": suite,
        "second_formatting": empty_string,
        "third_formatting": empty_string,
    },
    "ellipsis": {
        "first_formatting": empty_string,
        "second_formatting": empty_string,
    },
    "else": {
        "value": suite,
        "first_formatting": empty_string,
        "second_formatting": empty_string,
    },
    "endl": {
        "formatting": lambda value, key_name, node, state: _generator_to_string(_render_list(None, None, node["formatting"], state)),
    },
    "exec": {
        "fourth_formatting": empty_string,
    },
    "except": {
        "value": suite,
        "first_formatting": lambda value, key_name, node, state: " " if node["exception"] else "",
        "second_formatting": lambda value, key_name, node, state: " " if node["delimiter"] == "as" else "",
        "fourth_formatting": empty_string,
        "fifth_formatting": empty_string,
    },
    "finally": {
        "value": suite,
        "first_formatting": empty_string,
        "second_formatting": empty_string,
    },
    "for": {
        "value": suite,
        "fourth_formatting": empty_string,
        "fifth_formatting": empty_string,
    },
    "generator_comprehension": {
        "first_formatting": empty_string,
        "second_formatting": empty_string,
        "third_formatting": empty_string,
        "fourth_formatting": empty_string,
    },
    "getitem": {
        "first_formatting": empty_string,
        "second_formatting": empty_string,
        "third_formatting": empty_string,
        "fourth_formatting": empty_string,
    },
    "if": {
        "value": suite,
        "second_formatting": empty_string,
        "third_formatting": empty_string,
    },
    "lambda": {
        "first_formatting": lambda value, key_name, node, state: " " if node["arguments"] else "",
        "second_formatting": empty_string,
    },
    "list": {
        "value": dump_data_structure_body,
        "first_formatting": empty_string,
        "second_formatting": empty_string,
        "third_formatting": empty_string,
        "fourth_formatting": empty_string,
    },
    "list_argument": {
        "formatting": empty_string,
    },
    "list_comprehension": {
        "first_formatting": empty_string,
        "second_formatting": empty_string,
        "third_formatting": empty_string,
        "fourth_formatting": empty_string,
    },
    "raise": {
        "second_formatting": empty_string,
        "fourth_formatting": empty_string,
    },
    "return": {
        "formatting": lambda value, key_name, node, __: " " if node["value"] else ""
    },
    "set": {
        "value": dump_data_structure_body,
        "first_formatting": empty_string,
        "second_formatting": empty_string,
        "third_formatting": empty_string,
        "fourth_formatting": empty_string,
    },
    "set_comprehension": {
        "first_formatting": empty_string,
        "second_formatting": empty_string,
        "third_formatting": empty_string,
        "fourth_formatting": empty_string,
    },
    "string": {
        "first_formatting": empty_string,
        "second_formatting": empty_string,
    },
    "try": {
        "value": suite,
        "first_formatting": empty_string,
        "second_formatting": empty_string,
    },
    "tuple": {
        "value": dump_data_structure_body,
        "first_formatting": empty_string,
        "second_formatting": empty_string,
        "third_formatting": empty_string,
        "fourth_formatting": empty_string,
    },
    "unitary_operator": {
        "formatting": lambda value, key_name, node, __: " " if node["value"] == "not" else "",
    },
    "with": {
        "value": suite,
        "second_formatting": empty_string,
        "third_formatting": empty_string,
    },
    "yield": {
        "formatting": lambda value, key_name, node, __: " " if node["value"] else ""
    },
    "yield_atom": {
        "first_formatting": empty_string,
        "second_formatting": lambda value, key_name, node, __: " " if node["value"] else "",
        "third_formatting": empty_string,
    },
    "while": {
        "value": suite,
        "second_formatting": empty_string,
        "third_formatting": empty_string,
    },
}


def comment(node, state):
    to_return = ""
    logging.debug("%s %s" % ("==> previous:", state["previous"]))
    if state["previous"] and state["previous"]["type"] != "endl" and state["previous"] is not node:
        to_return += "  "
    if node["value"].startswith(("# ", "##", "#!")) or len(node["value"]) == 1:
        to_return += node["value"]
    else:
        to_return += "# " + node["value"][1:]

    return to_return


def print_(node, state):
    to_return = "print"

    if node["destination"]:
        to_return += " >>"
        to_return += _generator_to_string(_render_node(node["destination"], state))

    if node["value"]:
        value = _generator_to_string(_render_list(node["type"], "value", node["value"], state))
        if value.startswith("(") and value.endswith(")") and "," not in value:
            pass
        elif node["value"][0]["type"] != "comma":
            to_return += " "

        to_return += value

    return to_return


def endl(node, state):
    to_return = ""

    # replace tab with space
    indentation = node["indent"].replace("\t", " " * 8)

    # reindentation rules
    # self.indentation_stack store tuples ('found intentation', 'correct
    # indentation')
    if len(indentation) == 0:
        pass

    elif len(state["indentation_stack"]) == 0:
        if len(indentation) != 4:
            state["indentation_stack"].append((indentation, " " * 4))
            indentation = " " * 4
        else:
            state["indentation_stack"].append((indentation, indentation))

    elif indentation > state["indentation_stack"][-1][0]:
        if indentation != state["indentation_stack"][-1][1] + " " * 4:
            state["indentation_stack"].append(
                (indentation, state["indentation_stack"][-1][1] + " " * 4))
            indentation = state["indentation_stack"][-2][1] + " " * 4
        else:
            state["indentation_stack"].append((indentation, indentation))

    elif indentation < state["indentation_stack"][-1][0]:
        while state["indentation_stack"] and indentation != state["indentation_stack"][-1][0]:
            state["indentation_stack"].pop()
        if not state["indentation_stack"]:
            indentation = ""
        elif indentation != state["indentation_stack"][-1][1]:
            indentation = state["indentation_stack"][-1][1]

    elif indentation == state["indentation_stack"][-1][0]:
        indentation = state["indentation_stack"][-1][1]

    if find("comment", node["formatting"]):
        to_return += _generator_to_string(_render_list(None, None, node["formatting"], state))

    to_return += node["value"]
    to_return += indentation
    state["previous"] = node
    state["current_indent"] = node["indent"]
    return to_return


def import_(node, state):
    to_return = []

    for i in filter(lambda x: x["type"] != "comma", node["value"]):
        to_return.append("import " + _generator_to_string(_render_node(i, state)))

    return ("\n" + state["current_indent"]).join(to_return)


advanced_formatters = {
    "repr": lambda x, state: "repr(%s)" % _generator_to_string(_render_list(None, None, x["value"], state)),
    "comment": comment,
    "endl": endl,
    "import": import_,
    "print": print_,
}


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
