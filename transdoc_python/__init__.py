"""
# Transdoc Python

A Transdoc handler for Python docstrings, using libcst to rewrite
documentation.
"""

from importlib.metadata import version
from logging import getLogger
from pathlib import Path
from typing import IO

import libcst
import libcst as cst
from libcst import MetadataWrapper
from transdoc import TransdocHandler, TransdocTransformer
from transdoc.source_pos import SourcePos

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
        input_text = in_file.read()
        try:
            parsed = MetadataWrapper(cst.parse_module(input_text))
            visitor = DocstringVisitor(transformer, in_path)
            updated_cst = parsed.visit(visitor)
            visitor.raise_errors()
            if out_file is not None:
                out_file.write(updated_cst.code)
        except libcst.ParserSyntaxError:
            # Error while parsing the file
            # Just copy the file instead. We can safely transform it, since
            # while there is the risk of breaking Python syntax, the syntax is
            # already broken anyway, so it doesn't matter too much.
            # Perhaps this could cause issues if new Python syntax is
            # introduced that is unsupported by libcst. In this case, updating
            # libcst is the solution.
            # TODO: More-integrated way to warn of this
            log.warning(
                f"{in_path} failed to parse using libcst. "
                f"Transforming file as plaintext instead."
            )
            if out_file is not None:
                out_file.write(
                    transformer.transform(
                        input_text, in_path, SourcePos(1, 0)
                    )
                )


__all__ = [
    "__version__",
    "TransdocPythonHandler",
]


if __name__ == "__main__":
    handler: TransdocHandler = TransdocPythonHandler()
