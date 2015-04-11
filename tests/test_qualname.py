"""
Tests for the qualname module.
"""

from qualname import qualname


# These examples come from
# https://www.python.org/dev/peps/pep-3155/

class C:
    def f():
        pass

    class D:
        def g():
            pass


def f():
    def g():
        pass
    return g


def test_nested_classes():
    assert qualname(C) == 'C'
    assert qualname(C.f) == 'C.f'
    assert qualname(C.D) == 'C.D'
    assert qualname(C.D.g) == 'C.D.g'


def test_nested_functions():
    assert qualname(f) == 'f'
    assert qualname(f()) == 'f.<locals>.g'
