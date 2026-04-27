"""Directives that can be applied to both Sphinx and docutils."""

from __future__ import annotations

import typing as t

from docutils import nodes
from docutils.transforms import Transform
from docutils.transforms.references import Footnotes
from markdown_it.common.normalize_url import normalizeLink

from myst_parser._compat import findall
from myst_parser.mdit_to_docutils.base import clean_astext
from myst_parser.warnings_ import MystWarnings, create_warning


class UnreferencedFootnotesDetector(Transform):
    """Detect unreferenced footnotes and emit warnings.

    Replicates https://github.com/sphinx-doc/sphinx/pull/12730,
    but also allows for use in docutils (without sphinx).
    """

    default_priority = Footnotes.default_priority + 2

    # document: nodes.document

    def apply(self, **kwargs: t.Any) -> None:
        """Apply the transform."""
        pass


class SortFootnotes(Transform):
    """Sort auto-numbered, labelled footnotes by the order they are referenced.

    This is run before the docutils ``Footnote`` transform, where numbered labels are assigned.
    """

    default_priority = Footnotes.default_priority - 2

    # document: nodes.document

    def apply(self, **kwargs: t.Any) -> None:
        """Apply the transform."""
        pass


class CollectFootnotes(Transform):
    """Transform to move footnotes to the end of the document, and sort by label."""

    default_priority = Footnotes.default_priority + 3

    # document: nodes.document

    def apply(self, **kwargs: t.Any) -> None:
        """Apply the transform."""
        pass


class ResolveAnchorIds(Transform):
    """Transform for resolving `[name](#id)` type links."""

    default_priority = 879  # this is the same as Sphinx's StandardDomain.process_doc

    def apply(self, **kwargs: t.Any) -> None:
        """Apply the transform."""
        pass
