"""This module provides classes to Mock the core components of the docutils.RSTParser,
the key difference being that nested parsing treats the text as Markdown not rST.
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path
from typing import TYPE_CHECKING, Any

from docutils import nodes
from docutils.parsers.rst import Directive, DirectiveError
from docutils.parsers.rst import Parser as RSTParser
from docutils.parsers.rst.directives.misc import Include
from docutils.parsers.rst.states import Body, Inliner, RSTStateMachine
from docutils.statemachine import StringList
from docutils.utils import unescape

from .parsers.directives import MarkupError, parse_directive_text

if TYPE_CHECKING:
    from .mdit_to_docutils.base import DocutilsRenderer


class MockingError(Exception):
    """An exception to signal an error during mocking of docutils components."""


class MockInliner:
    """A mock version of `docutils.parsers.rst.states.Inliner`.

    This is parsed to role functions.
    """

    def __init__(self, renderer: DocutilsRenderer):
        """Initialize the mock inliner."""
        self._renderer = renderer
        # here we mock that the `parse` method has already been called
        # which is where these attributes are set (via the RST state Memo)
        self.document = renderer.document
        self.reporter = renderer.document.reporter
        self.language = renderer.language_module_rst
        self.parent = renderer.current_node

        if not hasattr(self.reporter, "get_source_and_line"):
            # In docutils this is set by `RSTState.runtime_init`
            self.reporter.get_source_and_line = lambda li: (self.document["source"], li)

        self.rfc_url = "rfc%d.html"

    def problematic(
        self, text: str, rawsource: str, message: nodes.system_message
    ) -> nodes.problematic:
        """Record a system message from parsing."""
        pass

    def parse(
        self, text: str, lineno: int, memo: Any, parent: nodes.Node
    ) -> tuple[list[nodes.Node], list[nodes.system_message]]:
        """Parse the text and return a list of nodes."""
        pass

    def __getattr__(self, name: str):
        """This method is only be called if the attribute requested has not
        been defined. Defined attributes will not be overridden.
        """
        # TODO use document.reporter mechanism?
        if hasattr(Inliner, name):
            msg = f"{type(self).__name__} has not yet implemented attribute '{name}'"
            raise MockingError(msg).with_traceback(sys.exc_info()[2])
        msg = f"{type(self).__name__} has no attribute {name}"
        raise MockingError(msg).with_traceback(sys.exc_info()[2])


class MockState:
    """A mock version of `docutils.parsers.rst.states.RSTState`.

    This is parsed to the `Directives.run()` method,
    so that they may run nested parses on their content that will be parsed as markdown,
    rather than RST.
    """

    def __init__(
        self,
        renderer: DocutilsRenderer,
        state_machine: MockStateMachine,
        lineno: int,
    ):
        self._renderer = renderer
        self._lineno = lineno
        self.document = renderer.document
        self.reporter = renderer.document.reporter
        self.state_machine = state_machine
        self.inliner = MockInliner(renderer)

        class Struct:
            document = self.document
            reporter = self.document.reporter
            language = renderer.language_module_rst
            title_styles: list[str] = []
            section_level = max(renderer._level_to_section)
            section_bubble_up_kludge = False
            inliner = self.inliner

        self.memo = Struct

    def parse_directive_block(
        self,
        content: StringList,
        line_offset: int,
        directive: type[Directive],
        option_presets: dict[str, Any],
    ) -> tuple[list[str], dict[str, Any], StringList, int]:
        """Parse the full directive text

        :raises MarkupError: for errors in parsing the directive
        :returns: (arguments, options, content, content_offset)
        """
        pass

    def nested_parse(
        self,
        block: StringList,
        input_offset: int,
        node: nodes.Element,
        match_titles: bool = False,
        state_machine_class=None,
        state_machine_kwargs=None,
    ) -> None:
        """Perform a nested parse of the input block, with ``node`` as the parent.

        :param block: The block of lines to parse.
        :param input_offset: The offset of the first line of block,
            to the starting line of the state (i.e. directive).
        :param node: The parent node to attach the parsed content to.
        :param match_titles: Whether to to allow the parsing of headings
            (normally this is false,
            since nested heading would break the document structure)
        """
        pass

    def parse_target(self, block, block_text, lineno: int):
        """
        Taken from https://github.com/docutils-mirror/docutils/blob/e88c5fb08d5cdfa8b4ac1020dd6f7177778d5990/docutils/parsers/rst/states.py#L1927
        """
        pass

    def inline_text(
        self, text: str, lineno: int
    ) -> tuple[list[nodes.Element], list[nodes.Element]]:
        """Parse text with only inline rules.

        :returns: (list of nodes, list of messages)
        """
        pass

    # U+2014 is an em-dash:
    attribution_pattern = re.compile("^((?:---?(?!-)|\u2014) *)(.+)")

    def block_quote(self, lines: list[str], line_offset: int) -> list[nodes.Element]:
        """Parse a block quote, which is a block of text,
        followed by an (optional) attribution.

        ::

           No matter where you go, there you are.

           -- Buckaroo Banzai
        """
        pass

    def build_table(self, tabledata, tableline, stub_columns: int = 0, widths=None):
        pass

    def build_table_row(self, rowdata, tableline):
        pass

    def nest_line_block_lines(self, block: nodes.line_block):
        """Modify the line block element in-place, to nest line block segments.

        Line nodes are placed into child line block containers, based on their indentation.
        """
        pass

    def _nest_line_block_segment(self, block: nodes.line_block):
        pass

    def __getattr__(self, name: str):
        """This method is only be called if the attribute requested has not
        been defined. Defined attributes will not be overridden.
        """
        cls = type(self).__name__
        msg = (
            f"{cls} has not yet implemented attribute '{name}'. "
            "You can parse RST directly via the `{{eval-rst}}` directive: "
            "https://myst-parser.readthedocs.io/en/latest/syntax/syntax.html#how-directives-parse-content"
            if hasattr(Body, name)
            else f"{cls} has no attribute '{name}'"
        )
        raise MockingError(msg).with_traceback(sys.exc_info()[2])


class MockStateMachine:
    """A mock version of `docutils.parsers.rst.states.RSTStateMachine`.

    This is parsed to the `Directives.run()` method.
    """

    def __init__(self, renderer: DocutilsRenderer, lineno: int):
        self._renderer = renderer
        self._lineno = lineno
        self.document = renderer.document
        self.language = renderer.language_module_rst
        self.reporter = self.document.reporter
        self.node: nodes.Element = renderer.current_node
        self.match_titles: bool = True

    def get_source(self, lineno: int | None = None):
        """Return document source path."""
        pass

    def get_source_and_line(self, lineno: int | None = None):
        """Return (source path, line) tuple for current or given line number."""
        pass

    def __getattr__(self, name: str):
        """This method is only be called if the attribute requested has not
        been defined. Defined attributes will not be overridden.
        """
        if hasattr(RSTStateMachine, name):
            msg = f"{type(self).__name__} has not yet implemented attribute '{name}'"
            raise MockingError(msg).with_traceback(sys.exc_info()[2])
        msg = f"{type(self).__name__} has no attribute {name}"
        raise MockingError(msg).with_traceback(sys.exc_info()[2])


class MockIncludeDirective:
    """This directive uses a lot of statemachine logic that is not yet mocked.
    Therefore, we treat it as a special case (at least for now).

    See:
    https://docutils.sourceforge.io/docs/ref/rst/directives.html#including-an-external-document-fragment
    """

    def __init__(
        self,
        renderer: DocutilsRenderer,
        name: str,
        klass: type[Include],
        arguments: list[str],
        options: dict[str, Any],
        body: list[str],
        lineno: int,
    ):
        self.renderer = renderer
        self.document = renderer.document
        self.name = name
        self.klass = klass
        self.arguments = arguments
        self.options = options
        self.body = body
        self.lineno = lineno

    def run(self) -> list[nodes.Element]:
        pass

    def add_name(self, node: nodes.Element):
        """Append self.options['name'] to node['names'] if it exists.

        Also normalize the name string and register it as explicit target.
        """
        pass


class MockRSTParser(RSTParser):
    """RSTParser which avoids a negative side effect."""

    def parse(self, inputstring: str, document: nodes.document):
        """Parse the input to populate the document AST."""
        pass
