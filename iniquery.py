"""
Interpret an ini style file into a queryable data structure.
"""
from squerly import Dict, Queryable
from iniparser import make_parser


def doc_meaning(pairs):
    doc = Dict()
    for mark in pairs:
        k, v = mark.value
        v.value.parent = doc
        doc[k.value] = v.value
    return doc


def section_meaning(pairs):
    return Dict((k.value, v.value) for k, v in pairs)


_parse = make_parser(doc_meaning, section_meaning)


def parse(data):
    return Queryable(_parse(data))
