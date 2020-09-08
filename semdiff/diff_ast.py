"""
AST and algorithms for diffing structures.
"""
import json
from itertools import zip_longest


class Prim:
    __slots__ = ("mark",)

    def __init__(self, mark):
        self.mark = mark

    def __lt__(self, other):
        return self.mark.value < other.mark.value

    def __eq__(self, other):
        try:
            return self.mark.value == other.mark.value
        except:
            pass
        return False

    def __hash__(self):
        return hash(self.mark.value)


class Name(Prim):
    pass


class Value(Prim):
    pass


class Node:
    __slots__ = ("name", "attrs", "children")

    def __init__(self, name=None, attrs=None, children=None):
        self.name = name
        self.attrs = attrs or tuple()
        self.children = children or tuple()

    def __lt__(self, other):
        if self.name == other.name:
            return self.attrs < other.attrs

        if self.name is None:
            return True

        if other.name is None:
            return False

        return self.name < other.name

    def __eq__(self, other):
        self.name == other.name and self.attrs == other.attrs and self.children == other.children


class Diff:
    def __init__(self, left, right):
        self.left = left
        self.right = right


def unique_name_diff(left, right):
    """
    Diff structures that have unique names at each level and for which order
    doesn't matter. i.e. simple key/value pairs, dicts from json, etc.
    """
    if not (left and right):
        return [Diff(left, right)]

    res = []

    if left.name != right.name:
        res.append(Diff(left.name, right.name))

    res.extend(Diff(l, r) for (l, r) in zip_longest(left.attrs, right.attrs) if l != r)

    left_names = {l.name: l for l in left.children}
    right_names = {r.name: r for r in right.children}

    for k, v in left_names.items():
        if k not in right_names:
            res.append(Diff(v.name, None))

    for k, v in right_names.items():
        if k not in left_names:
            res.append(Diff(None, v.name))

    for k in left_names.keys() & right_names.keys():
        res.extend(unique_name_diff(left_names[k], right_names[k]))

    return res


class NodeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Node):
            return {
                "name": self.default(obj.name) if obj.name is not None else {},
                "attrs": [self.default(a) for a in obj.attrs],
                "children": [self.default(c) for c in obj.children]
            }
        elif isinstance(obj, Prim):
            return {
                "lineno": obj.mark.lineno,
                "col": obj.mark.col,
                "value": obj.mark.value,
                "start": obj.mark.start,
                "end": obj.mark.end,
            }
        elif isinstance(obj, Diff):
            return {
                "left": self.default(obj.left) if obj.left else None,
                "right": self.default(obj.right) if obj.right else None,
            }
        return super().default(obj)
