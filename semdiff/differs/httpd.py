"""
Interpret an httpd style file into a tree that can be diffed.
"""
from semdiff.diff_ast import Name, Node, Value
from semdiff.differs import differ
from semdiff.grammars.httpd import make_parser


def _section_meaning(tag, children):
    name, attrs = tag
    attrs = tuple(Value(v) for v in attrs)
    return Node(Name(name), attrs=attrs, children=children)


def _directive_meaning(name, attrs):
    attrs = tuple(Value(v) for v in attrs)
    return Node(Name(name), attrs=attrs)


_parser = make_parser(_section_meaning, _directive_meaning)


def _parse(data):
    res = _parser(data)
    return Node(children=res)


@differ("httpd")
def diff(l, r):
    left = _parse(l)  # noqa
    right = _parse(r)  # noqa
    # TODO: call some diff algo
