"""Overrides to ``sphinx.ext.mathjax``

This fixes two issues:

1. Mathjax should not search for ``$`` delimiters, nor LaTeX amsmath environments,
   since we already achieve this with the dollarmath and amsmath mrakdown-it-py plugins
2. amsmath math blocks should be wrapped in mathjax delimiters (default ``\\[...\\]``),
   and assigned an equation number

"""

from docutils import nodes
from sphinx.application import Sphinx
from sphinx.ext import mathjax
from sphinx.locale import _
from sphinx.util import logging
from sphinx.util.math import get_node_equation_number
from sphinx.writers.html import HTMLTranslator

logger = logging.getLogger(__name__)


def log_override_warning(app: Sphinx, version: int, current: str, new: str) -> None:
    """Log a warning if MathJax configuration being overridden."""
    pass


def override_mathjax(app: Sphinx):
    """Override aspects of the mathjax extension.

    MyST-Parser parses dollar and latex math, via markdown-it plugins.
    Therefore, we tell Mathjax to only render these HTML elements.
    This is accompanied by setting the `ignoreClass` on the top-level section of each MyST document.
    """
    pass


def html_visit_displaymath(self: HTMLTranslator, node: nodes.math_block) -> None:
    """Override for sphinx.ext.mathjax.html_visit_displaymath to handle amsmath.

    By default displaymath, are normally wrapped in a prefix/suffix,
    defined by mathjax_display, and labelled nodes are numbered.
    However, this is not the case if the math_block is set as 'nowrap', as for amsmath.
    Therefore, we need to override this behaviour.
    """
    pass
