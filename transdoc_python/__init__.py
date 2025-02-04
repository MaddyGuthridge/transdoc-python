"""
# Transdoc Python

A Transdoc handler for Python docstrings, using libcst to rewrite
documentation.
"""

from importlib.metadata import version
from logging import getLogger
from pathlib import Path
from typing import IO
import libcst as cst
from libcst import MetadataWrapper
import libcst
from transdoc import TransdocHandler, TransdocTransformer

from transdoc_python.__visitor import DocstringVisitor


__version__ = version("transdoc-python")


log = getLogger("transdoc-python")


class TransdocPythonHandler:
    """
    A Transdoc handler for Python docstrings.
    """

    def __repr__(self) -> str:
        return "TransdocPythonHandler"

    def matches_file(self, file_path: str) -> bool:
        return Path(file_path).suffix in [".py", ".pyi"]

    def transform_file(
        self,
        transformer: TransdocTransformer,
        in_path: str,
        in_file: IO,
        out_file: IO | None,
    ) -> None:
        try:
            parsed = MetadataWrapper(cst.parse_module(in_file.read()))
            visitor = DocstringVisitor(transformer, in_path)
            updated_cst = parsed.visit(visitor)
            visitor.raise_errors()
            if out_file is not None:
                out_file.write(updated_cst.code)
        except libcst.ParserSyntaxError:
            # Error while parsing the file
            # Just copy the file instead
            # TODO: More-integrated way to warn of this
            log.warning(
                f"{in_path} failed to parse using libcst. Copying file as-is instead."
            )
            if out_file is not None:
                out_file.write(in_file.read())


__all__ = [
    "__version__",
    "TransdocPythonHandler",
]


if __name__ == "__main__":
    handler: TransdocHandler = TransdocPythonHandler()
