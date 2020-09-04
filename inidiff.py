"""
Interpret an ini style file into a tree that can be diffed.
"""
from iniparser import make_parser
from nodes import Name, Node, Value, unique_name_diff


def doc_meaning(data):
    res = []
    for mark in data:
        k, v = mark.value
        k.end = mark.end
        res.append(Node(name=Name(k), children=v.value))
    return Node(children=tuple(res))


def section_meaning(pairs):
    return tuple(Node(name=Name(k), attrs=(Value(v),)) for k, v in pairs)


parse = make_parser(doc_meaning, section_meaning)


def diff_structure(l, r):
    return unique_name_diff(parse(l), parse(r))
