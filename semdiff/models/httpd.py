"""
Interpret an ini style file into a queryable data structure.
"""
from parsr.query import Directive, Entry, Section
from semdiff.grammars.httpd import make_parser


def section_meaning(tag, children, endtag):
    name, attrs = tag.value
    attrs = [a.value for a in attrs]
    return Section(name=name.value, attrs=attrs, children=children.value, lineno=name.lineno)


def directive_meaning(name, attrs):
    attrs = [a.value for a in attrs]
    return Directive(name=name.value, attrs=attrs, lineno=name.lineno)


_parser = make_parser(section_meaning, directive_meaning)


def parse(data):
    res = _parser(data)
    return Entry(children=res)
