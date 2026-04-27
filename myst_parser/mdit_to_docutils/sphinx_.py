"""Convert Markdown-it tokens to docutils nodes, including sphinx specific elements."""

from __future__ import annotations

import os
from pathlib import Path
from typing import cast
from uuid import uuid4

from docutils import nodes
from markdown_it.tree import SyntaxTreeNode
from sphinx import addnodes
from sphinx.domains.math import MathDomain
from sphinx.environment import BuildEnvironment
from sphinx.ext.intersphinx import InventoryAdapter
from sphinx.util import logging

from myst_parser import inventory
from myst_parser.mdit_to_docutils.base import DocutilsRenderer, token_line
from myst_parser.warnings_ import MystWarnings

LOGGER = logging.getLogger(__name__)


class SphinxRenderer(DocutilsRenderer):
    """A markdown-it-py renderer to populate (in-place) a `docutils.document` AST.

    This is sub-class of `DocutilsRenderer` that handles sphinx specific aspects,
    such as cross-referencing.
    """

    @property
    def sphinx_env(self) -> BuildEnvironment:
        pass

    def _process_wrap_node(
        self,
        wrap_node: nodes.Element,
        token: SyntaxTreeNode,
        explicit: bool,
        classes: list[str],
        path_dest: str,
    ):
        """Process a wrap node, which is a node that wraps a link."""
        pass

    def _handle_relative_docs(self, destination: str) -> str:
        """Make the path relative to an "including" document

        This is set when using the `relative-docs` option of the MyST `include` directive
        """
        pass

    def render_link_project(self, token: SyntaxTreeNode) -> None:
        pass

    def render_link_path(self, token: SyntaxTreeNode) -> None:
        pass

    def render_link_unknown(self, token: SyntaxTreeNode) -> None:
        """Render link token `[text](link "title")`,
        where the link has not been identified as an external URL.
        """
        pass

    def get_inventory_matches(
        self,
        *,
        invs: str | None,
        domains: str | None,
        otypes: str | None,
        target: str | None,
    ) -> list[inventory.InvMatch]:
        pass

    def render_math_block_label(self, token: SyntaxTreeNode) -> None:
        """Render math with referenceable labels, e.g. ``$a=1$ (label)``."""
        pass

    def _random_label(self) -> str:
        pass

    def render_amsmath(self, token: SyntaxTreeNode) -> None:
        """Renderer for the amsmath extension."""
        pass

    def add_math_target(self, node: nodes.math_block) -> nodes.target:
        # Code mainly copied from sphinx.directives.patches.MathDirective

        # register label to domain
        pass
