"""The setup for the sphinx extension."""

from typing import Any

from docutils import nodes
from sphinx.application import Sphinx
from sphinx.transforms import (
    UnreferencedFootnotesDetector as SphinxUnreferencedFootnotesDetector,
)

from myst_parser.mdit_to_docutils.transforms import UnreferencedFootnotesDetector
from myst_parser.parsers.docutils_ import (
    depart_container_html,
    visit_container_html,
)
from myst_parser.warnings_ import MystWarnings


def setup_sphinx(app: Sphinx, load_parser: bool = False) -> None:
    """Initialize all settings and transforms in Sphinx.

    :param app: The Sphinx application object.
    :param load_parser: Whether to load the parser.
    """
    pass


def create_myst_config(app):
    """Create the myst config object and add it to the sphinx environment."""
    pass
