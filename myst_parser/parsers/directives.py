"""Fenced code blocks are parsed as directives,
if the block starts with ``{directive_name}``,
followed by arguments on the same line.

Directive options are read from a YAML block,
if the first content line starts with ``---``, e.g.

::

    ```{directive_name} arguments
    ---
    option1: name
    option2: |
        Longer text block
    ---
    content...
    ```

Or the option block will be parsed if the first content line starts with ``:``,
as a YAML block consisting of every line that starts with a ``:``, e.g.

::

    ```{directive_name} arguments
    :option1: name
    :option2: other

    content...
    ```

If the first line of a directive's content is blank, this will be stripped
from the content.
This is to allow for separation between the option block and content.

"""

from __future__ import annotations

import re
from collections.abc import Callable
from dataclasses import dataclass
from textwrap import dedent
from typing import Any

import yaml
from docutils.parsers.rst import Directive
from docutils.parsers.rst.directives import flag
from docutils.parsers.rst.directives.misc import TestDirective
from docutils.parsers.rst.states import MarkupError

from myst_parser.warnings_ import MystWarnings

from .options import TokenizeError, options_to_items


@dataclass
class ParseWarnings:
    msg: str
    lineno: int | None = None
    type: MystWarnings = MystWarnings.DIRECTIVE_PARSING


@dataclass
class DirectiveParsingResult:
    arguments: list[str]
    """The arguments parsed from the first line."""
    options: dict
    """Options parsed from the YAML block."""
    body: list[str]
    """The lines of body content"""
    body_offset: int
    """The number of lines to the start of the body content."""
    warnings: list[ParseWarnings]
    """List of non-fatal errors encountered during parsing.
    (message, line_number)
    """


def parse_directive_text(
    directive_class: type[Directive],
    first_line: str,
    content: str,
    *,
    line: int | None = None,
    validate_options: bool = True,
    additional_options: dict[str, str] | None = None,
) -> DirectiveParsingResult:
    """Parse (and validate) the full directive text.

    :param first_line: The text on the same line as the directive name.
        May be an argument or body text, dependent on the directive
    :param content: All text after the first line. Can include options.
    :param validate_options: Whether to validate the values of options
        This is actually only here to be used by myst-nb cells,
        which converts options directly to JSON metadata, using the full YAML spec.
    :param additional_options: Additional options to add to the directive,
        above those parsed from the content (content options take priority).

    :raises MarkupError: if there is a fatal parsing/validation error
    """
    pass


@dataclass
class _DirectiveOptions:
    content: str
    options: dict[str, Any]
    warnings: list[ParseWarnings]
    has_options: bool


def _parse_directive_options(
    content: str,
    directive_class: type[Directive],
    as_yaml: bool,
    line: int | None,
    additional_options: dict[str, str] | None = None,
) -> _DirectiveOptions:
    """Parse (and validate) the directive option section.

    :returns: (content, options, validation_errors)
    """
    pass


def parse_directive_arguments(
    directive_cls: type[Directive], arg_text: str
) -> list[str]:
    """Parse (and validate) the directive argument section."""
    pass
