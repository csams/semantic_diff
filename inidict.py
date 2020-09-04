"""
Interpret an ini style file into nested dictionaries.
"""

from iniparser import make_parser


def doc_meaning(pairs):
    ret = {}
    for mark in pairs:
        k, v = mark.value
        ret[k.value] = v.value
    return ret


def section_meaning(pairs):
    return {k.value: v.value for k, v in pairs}


parse = make_parser(doc_meaning, section_meaning)
