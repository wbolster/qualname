"""
Module to find out the qualified name of a class.

In Python 3, classes have a ``__qualname__`` property. Unfortunately,
Python 2 does not have an obvious equivalent. This module uses source
code inspection to figure out how a (nested) class is defined in order
to determine the qualified name for it.

https://www.python.org/dev/peps/pep-3155/
"""

import ast
import inspect

__all__ = ['qualname']

_cache = {}


class _Visitor(ast.NodeVisitor):
    def __init__(self):
        self.stack = []
        self.qualnames = {}

    def store_qualname(self, lineno):
        qn = ".".join(n for n in self.stack)
        self.qualnames[lineno] = qn

    def visit_ClassDef(self, node):
        self.stack.append(node.name)
        self.store_qualname(node.lineno)
        self.generic_visit(node)
        self.stack.pop()


def qualname(cls):
    """Find out the qualified name for a class."""

    # For Python 3.3+, this is straight-forward.
    if hasattr(cls, '__qualname__'):
        return cls.__qualname__

    # For older Python version, things get complicated.
    mod = inspect.getmodule(cls)
    if mod is None:
        return cls.__name__

    filename = getattr(mod, '__file__', None)
    if filename is None:
        return cls.__name__

    try:
        lines, lineno = inspect.getsourcelines(cls)
    except (OSError, IOError):
        return cls.__name__

    qualnames = _cache.get(filename)
    if qualnames is None:
        with open(filename, 'r') as fp:
            source = fp.read()
        node = ast.parse(source, filename)
        visitor = _Visitor()
        visitor.visit(node)
        _cache[filename] = qualnames = visitor.qualnames

    qn = qualnames.get(lineno)
    if qn is None:
        return cls.__name__

    return qn
