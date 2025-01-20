"""
# Transdoc Python / Visitor

LibCST visitor
"""

import libcst as cst
from libcst.metadata import PositionProvider
from transdoc import TransdocTransformer
from transdoc.source_pos import SourcePos


class DocstringVisitor(cst.CSTTransformer):
    """
    Rewrite documentation.
    """

    METADATA_DEPENDENCIES = (PositionProvider,)

    def __init__(
        self, transformer: TransdocTransformer, filename: str
    ) -> None:
        """
        Create an instance of the doc transformer module
        """
        self.__transformer = transformer
        self.__filename = filename
        self.__errors: list[Exception] = []

    def raise_errors(self) -> None:
        """
        If any errors occurred when visiting the code, raise them.
        """
        if len(self.__errors):
            raise ExceptionGroup(
                f"Errors occurred when transforming file {self.__filename}",
                self.__errors,
            )

    def leave_SimpleString(
        self,
        original_node: cst.SimpleString,
        updated_node: cst.SimpleString,
    ) -> cst.BaseExpression:
        """
        After visiting a string, check if it is a triple-quoted string. If so,
        apply formatting to it.

        Currently, I'm assuming that all triple-quoted strings are docstrings
        so that we can handle attribute docstrings (which otherwise don't work
        very nicely).
        """
        node_pos = self.get_metadata(PositionProvider, original_node).start
        # FIXME: Figure out indentation a little more-reliably (ie respecting
        # tabs)
        indentation = node_pos.column * " "
        if original_node.quote in ['"""', "'''"]:
            try:
                processed = self.__transformer.transform(
                    updated_node.value,
                    self.__filename,
                    SourcePos(node_pos.line, node_pos.column),
                    indentation,
                )
            except Exception as e:
                self.__errors.append(e)

            return updated_node.with_changes(value=processed)
        return updated_node
