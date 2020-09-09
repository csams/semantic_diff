"""
Interpret an httpd style file into a tree that can be diffed.
"""
from semdiff.diff_ast import Name, Node, Value, structure_diff
from semdiff.differs import differ
from semdiff.grammars.httpd import make_parser


def _section_meaning(tag, children, endtag):
    name, attrs = tag
    name.end = endtag.end
    attrs = tuple(Value(v) for v in attrs)
    return Node(Name(name), attrs=attrs, children=children.value)


def _directive_meaning(name, attrs):
    if attrs:
        name.end = attrs[-1].end
    attrs = tuple(Value(v) for v in attrs)
    return Node(Name(name), attrs=attrs)


_parser = make_parser(_section_meaning, _directive_meaning)


def _parse(data):
    res = _parser(data)
    return Node(children=res)


@differ("httpd")
def diff(l, r):
    return structure_diff(_parse(l), _parse(r), dup_names=True)
