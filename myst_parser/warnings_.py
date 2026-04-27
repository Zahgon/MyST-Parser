"""Central handling of warnings for the myst extension."""

from __future__ import annotations

from collections.abc import Sequence
from enum import Enum

from docutils import nodes, utils


class MystWarnings(Enum):
    """MyST warning types."""

    DEPRECATED = "deprecated"
    """Deprecated usage."""
    NOT_SUPPORTED = "not_supported"
    """Functionality that is not yet supported in docutils."""

    RENDER_METHOD = "render"
    """The render method is not implemented."""

    MD_TOPMATTER = "topmatter"
    """Issue reading front-matter."""
    MD_DEF_DUPE = "duplicate_def"
    """Duplicate Markdown reference definition."""
    MD_HEADING_NON_CONSECUTIVE = "header"
    """Non-consecutive heading levels."""

    DIRECTIVE_PARSING = "directive_parse"
    """Issue parsing directive."""
    DIRECTIVE_OPTION = "directive_option"
    """Issue parsing directive options."""
    DIRECTIVE_OPTION_COMMENTS = "directive_comments"
    """Directive options has # comments, which may not be supported in future versions."""
    DIRECTIVE_BODY = "directive_body"
    """Issue parsing directive body."""
    UNKNOWN_DIRECTIVE = "directive_unknown"
    """Unknown directive."""
    UNKNOWN_ROLE = "role_unknown"
    """Unknown role."""

    # cross-reference resolution
    XREF_AMBIGUOUS = "xref_ambiguous"
    """Multiple targets were found for a cross-reference."""
    XREF_MISSING = "xref_missing"
    """A target was not found for a cross-reference."""
    INV_LOAD = "inv_retrieval"
    """Failure to retrieve or load an inventory."""
    IREF_MISSING = "iref_missing"
    """A target was not found for an inventory reference."""
    IREF_AMBIGUOUS = "iref_ambiguous"
    """Multiple targets were found for an inventory reference."""
    LEGACY_DOMAIN = "domains"
    """A legacy domain found, which does not support `resolve_any_xref`."""

    # extensions
    HEADING_SLUG = "heading_slug"
    """An error occurred computing a heading slug."""
    STRIKETHROUGH = "strikethrough"
    """Strikethrough warning, since only implemented in HTML."""
    HTML_PARSE = "html"
    """HTML could not be parsed."""
    INVALID_ATTRIBUTE = "attribute"
    """Invalid attribute value."""
    SUBSTITUTION = "substitution"
    """Substitution could not be resolved."""


def _is_suppressed_warning(
    type: str, subtype: str, suppress_warnings: Sequence[str]
) -> bool:
    """Check whether the warning is suppressed or not.

    Mirrors:
    https://github.com/sphinx-doc/sphinx/blob/47d9035bca9e83d6db30a0726a02dc9265bd66b1/sphinx/util/logging.py
    """
    pass


def create_warning(
    document: nodes.document,
    message: str,
    subtype: MystWarnings | str,
    *,
    wtype: str | None = None,
    node: nodes.Element | None = None,
    line: int | None = None,
    append_to: nodes.Element | None = None,
) -> nodes.system_message | None:
    """Generate a warning, logging if it is necessary.

    If the warning type is listed in the ``suppress_warnings`` configuration,
    then ``None`` will be returned and no warning logged.
    """
    pass


def _create_warning_node(
    msg: str, source: str, line: int | None
) -> nodes.system_message:
    pass
