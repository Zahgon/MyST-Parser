"""Code to use internally, for documentation."""

from __future__ import annotations

import contextlib
import io
from collections.abc import Sequence
from typing import Union, get_args, get_origin

from docutils import nodes
from docutils.core import Publisher
from docutils.parsers.rst import directives
from sphinx.directives import other
from sphinx.transforms.post_transforms import SphinxPostTransform
from sphinx.util import logging
from sphinx.util.docutils import SphinxDirective

from myst_parser.parsers.docutils_ import to_html5_demo

from .config.main import MdParserConfig
from .parsers.docutils_ import Parser as DocutilsParser
from .warnings_ import MystWarnings

LOGGER = logging.getLogger(__name__)


class StripUnsupportedLatex(SphinxPostTransform):
    """Remove unsupported nodes from the doctree."""

    default_priority = 900

    def run(self, **kwargs):
        pass


class NumberSections(SphinxPostTransform):
    """Number sections (html only)"""

    default_priority = 710  # same as docutils.SectNum
    formats = ("html",)

    def run(self, **kwargs):
        pass


class _ConfigBase(SphinxDirective):
    """Directive to automate rendering of the configuration."""

    @staticmethod
    def table_header():
        pass

    @staticmethod
    def field_default(value):
        pass

    @staticmethod
    def field_type(field):
        pass


class MystConfigDirective(_ConfigBase):
    option_spec = {
        "sphinx": directives.flag,
        "extensions": directives.flag,
        "scope": lambda x: directives.choice(x, ["global", "local"]),
    }

    def run(self):
        """Run the directive."""
        pass


class DocutilsCliHelpDirective(SphinxDirective):
    """Directive to print the docutils CLI help."""

    has_content = False
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = False

    def run(self):
        """Run the directive."""
        pass


class DirectiveDoc(SphinxDirective):
    """Load and document a directive."""

    required_arguments = 1  # name of the directive
    has_content = True

    def run(self):
        """Run the directive."""
        pass


def convert_opt(name, func):
    """Convert an option function to a string."""
    pass


class MystWarningsDirective(SphinxDirective):
    """Directive to print all known warnings."""

    has_content = False
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = False

    def run(self):
        """Run the directive."""
        pass


class MystExampleDirective(SphinxDirective):
    """Directive to create an example, showing the source and output."""

    has_content = True
    option_spec = {
        "alt-output": directives.unchanged,
        "highlight": directives.unchanged,
        # "html": directives.flag,
    }

    def run(self):
        """Run the directive."""
        pass


class MystAdmonitionDirective(SphinxDirective):
    """Directive to show a set of admonitions, in a tab set."""

    required_arguments = 1
    final_argument_whitespace = True

    def run(self):
        """Run the directive."""
        pass


class MystToHTMLDirective(SphinxDirective):
    """Directive to convert MyST to HTML."""

    has_content = True
    optional_arguments = 1
    final_argument_whitespace = True
    option_spec = {
        "extensions": directives.unchanged,
    }

    def run(self):
        """Run the directive."""
        pass


### MyST Lexer ###
# TODO when some more work and testing, this should be made available publicly

from pygments import token  # noqa: E402
from pygments.lexer import bygroups, inherit, this, using  # noqa: E402
from pygments.lexers.markup import MarkdownLexer  # noqa: E402


class MystLexer(MarkdownLexer):
    """A custom lexer for MyST Markdown."""

    name = "MyST"
    aliases = ["myst"]
    filenames = ["*.myst"]
    mimetypes = ["text/x-myst"]

    tokens = {
        "root": [
            # (target)=
            (
                r"^(\()([^\n]+)(\)=)(\n)",
                bygroups(
                    token.Punctuation, token.Name.Label, token.Punctuation, token.Text
                ),
            ),
            # :::
            (r"^([\:]{3,})(\n)", bygroups(token.Punctuation, token.Text)),
            # :::name other
            # TODO this seems to "eat" the next line
            # (r"^([\:]{3,})([^\s\n]+)(\s+)([^\n]+)(\n)",
            # bygroups(token.Punctuation, token.Name.Tag, token.Whitespace, token.Text,token.Text)),
            # :::name
            (
                r"^([\:]{3,})([^\n]+)(\n)",
                bygroups(token.Punctuation, token.Name.Tag, token.Text),
            ),
            # :name: value
            (
                r"^(\:)([^\n\:]+)(\:)([^\n]+)(\n)",
                bygroups(
                    token.Punctuation,
                    token.Generic.Strong,
                    token.Punctuation,
                    using(this, state="inline"),
                    token.Text,
                ),
            ),
            inherit,
        ],
        "inline": [
            # escape (we have to copy this from the parent class)
            (r"\\.", token.Text),
            # {name}
            (
                r"(\{)([a-zA-Z0-9+:-]+)(\})",
                bygroups(token.Punctuation, token.Operator.Word, token.Punctuation),
            ),
            # <http:example.com>
            (
                r"(<)(http|https|mailto|project|path|inv)(\:)([^\s>]+)(>)",
                bygroups(
                    token.Punctuation,
                    token.String.Other,
                    token.String.Other,
                    token.Name.Label,
                    token.Punctuation,
                ),
            ),
            inherit,
        ],
    }
