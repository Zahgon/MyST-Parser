"""Convert HTML to docutils nodes."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

from docutils import nodes

from myst_parser.parsers.parse_html import Data, tokenize_html
from myst_parser.warnings_ import MystWarnings

if TYPE_CHECKING:
    from .base import DocutilsRenderer


def make_error(
    document: nodes.document, error_msg: str, text: str, line_number: int
) -> nodes.system_message:
    pass


OPTION_KEYS_IMAGE = {"class", "alt", "height", "width", "align", "name"}
# note: docutils also has scale and target

OPTION_KEYS_ADMONITION = {"class", "name"}

# See https://github.com/micromark/micromark-extension-gfm-tagfilter
RE_FLOW = re.compile(
    r"<(\/?)(iframe|noembed|noframes|plaintext|script|style|title|textarea|xmp)(?=[\t\n\f\r />])",
    re.IGNORECASE,
)


def default_html(text: str, source: str, line_number: int) -> list[nodes.Element]:
    pass


def html_to_nodes(
    text: str, line_number: int, renderer: DocutilsRenderer
) -> list[nodes.Element]:
    """Convert HTML to docutils nodes."""
    pass
