"""
Interpret an ini style file into a tree that can be diffed.
"""
from semdiff.grammars.ini import make_parser
from semdiff.diff_ast import Name, Node, Value, unique_name_diff
from semdiff.differs import differ


def _doc_meaning(data):
    res = []
    for mark in data:
        k, v = mark.value
        k.end = mark.end
        res.append(Node(name=Name(k), children=v.value))
    return Node(children=tuple(res))


def _section_meaning(pairs):
    return tuple(Node(name=Name(k), attrs=(Value(v),)) for k, v in pairs)


_parse = make_parser(_doc_meaning, _section_meaning)


@differ("ini")
def diff(l, r):
    return unique_name_diff(_parse(l), _parse(r))
