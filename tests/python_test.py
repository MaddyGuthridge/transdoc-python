"""
# Tests / Python test

Test cases for transforming Python code.
"""

from inspect import getsource

import jestspectation as expect
import pytest
from transdoc import TransdocTransformer, get_all_handlers, transform

from transdoc_python import TransdocPythonHandler


def test_transdoc_python_is_registered():
    """The handler is automatically registered with Transdoc"""
    handlers = get_all_handlers()
    assert handlers == expect.ListContaining(
        [expect.Any(TransdocPythonHandler)]
    )


def hello(name: str) -> str:
    """
    Says hello to someone.

    Example: {{hello[Maddy]}}
    """
    return f"Hello, {name}"


expected = '''
def hello(name: str) -> str:
    """
    Says hello to someone.

    Example: Hello, Maddy
    """
    return f"Hello, {name}"
'''.lstrip()


def test_transforms_python():
    """Ensure the handler correctly processes"""
    transformer = TransdocTransformer({"hello": hello})
    assert (
        transform(
            transformer,
            getsource(hello),
            path="hello.py",
            handler=TransdocPythonHandler(),
        )
        == expected
    )


def err(msg: str) -> str:
    """
    Raise an exception with the given error.

    Example: {{err[An intentional error]}}
    """
    raise Exception(msg)


def test_gracefully_handles_errors():
    """
    Ensure that errors are handled gracefully (raised in an ExceptionGroup).
    """
    transformer = TransdocTransformer({"err": err})
    with pytest.raises(ExceptionGroup) as excinfo:
        transform(
            transformer,
            getsource(err),
            path="err.py",
            handler=TransdocPythonHandler(),
        )

    assert excinfo.group_contains(Exception)
