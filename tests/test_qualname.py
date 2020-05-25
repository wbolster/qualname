"""
Tests for the qualname module.
"""
import pytest

from qualname import qualname

# These examples are based on the examples from
# https://www.python.org/dev/peps/pep-3155/

class C(object):
    @staticmethod
    def f():
        pass

    class D(object):
        @staticmethod
        def g():
            pass

        @staticmethod
        def h():
            def i():
                def j():
                    pass
                return j
            return i()


def f():
    def g():
        pass
    return g


def test_nested_classes():
    assert qualname(C) == 'C'
    assert qualname(C.D) == 'C.D'


def test_methods_in_nested_classes():
    assert qualname(C.f) == 'C.f'
    assert qualname(C.D.g) == 'C.D.g'


def test_nested_functions():
    assert qualname(f) == 'f'
    assert qualname(f()) == 'f.<locals>.g'
    assert qualname(C.D.h()) == 'C.D.h.<locals>.i.<locals>.j'


def test_builtin():
    assert qualname(int) == 'int'
    assert qualname(DeprecationWarning) == 'DeprecationWarning'


def test_no_source_file():
    code = compile("lambda x: 12", __file__, "eval")
    with pytest.raises(AttributeError):
        qualname(code)

    fn = eval(code)
    with pytest.raises(AttributeError):
        qualname(code)
