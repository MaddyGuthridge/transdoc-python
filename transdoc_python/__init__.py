"""
# Transdoc Python

A Transdoc handler for Python docstrings, using libcst to rewrite
documentation.
"""

from pathlib import Path
from typing import IO
import libcst as cst
from libcst import MetadataWrapper
from transdoc import TransdocHandler, TransdocTransformer

from transdoc_python.__visitor import DocstringVisitor


class TransdocPythonHandler:
    """
    A Transdoc handler for Python docstrings.
    """

    def matches_file(self, file_path: str) -> bool:
        return Path(file_path).suffix in [".py", ".pyi"]

    def transform_file(
        self,
        transformer: TransdocTransformer,
        in_path: str,
        in_file: IO,
        out_file: IO | None,
    ) -> None:
        parsed = MetadataWrapper(cst.parse_module(in_file.read()))
        visitor = DocstringVisitor(transformer, in_path)
        updated_cst = parsed.visit(visitor)
        visitor.raise_errors()
        if out_file is not None:
            out_file.write(updated_cst.code)


if __name__ == "__main__":
    handler: TransdocHandler = TransdocPythonHandler()
