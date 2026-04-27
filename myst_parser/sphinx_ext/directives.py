"""MyST specific directives"""

from __future__ import annotations

from copy import copy
from typing import cast

from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.directives import SphinxDirective
from sphinx.util.docutils import SphinxRole

from myst_parser.mocking import MockState


def align(argument):
    pass


def figwidth_value(argument):
    pass


class SubstitutionReferenceRole(SphinxRole):
    """Implement substitution references as a role.

    Note, in ``docutils/parsers/rst/roles.py`` this is left unimplemented.
    """

    def run(self) -> tuple[list[nodes.Node], list[nodes.system_message]]:
        pass


class FigureMarkdown(SphinxDirective):
    """Directive for creating a figure with Markdown compatible syntax.

    Example::

        :::{figure-md} target
        <img src="img/fun-fish.png" alt="fishy" class="bg-primary mb-1" width="200px">

        This is a caption in **Markdown**
        :::

    """

    required_arguments = 0
    optional_arguments = 1  # image target
    final_argument_whitespace = True
    has_content = True

    option_spec = {
        "width": figwidth_value,
        "class": directives.class_option,
        "align": align,
        "name": directives.unchanged,
    }

    def run(self) -> list[nodes.Node]:
        pass

    def figure_error(self, message):
        """A warning for reporting an invalid figure."""
        pass
