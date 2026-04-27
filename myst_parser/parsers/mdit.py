"""This module holds the ``create_md_parser`` function,
which creates a parser from the config.
"""

from __future__ import annotations

from collections.abc import Callable

from markdown_it import MarkdownIt
from markdown_it.renderer import RendererProtocol
from mdit_py_plugins.amsmath import amsmath_plugin
from mdit_py_plugins.attrs import attrs_block_plugin, attrs_plugin
from mdit_py_plugins.colon_fence import colon_fence_plugin
from mdit_py_plugins.deflist import deflist_plugin
from mdit_py_plugins.dollarmath import dollarmath_plugin
from mdit_py_plugins.field_list import fieldlist_plugin
from mdit_py_plugins.footnote import footnote_plugin
from mdit_py_plugins.front_matter import front_matter_plugin
from mdit_py_plugins.myst_blocks import myst_block_plugin
from mdit_py_plugins.myst_role import myst_role_plugin
from mdit_py_plugins.substitution import substitution_plugin
from mdit_py_plugins.tasklists import tasklists_plugin
from mdit_py_plugins.wordcount import wordcount_plugin

from myst_parser.config.main import MdParserConfig


def create_md_parser(
    config: MdParserConfig, renderer: Callable[[MarkdownIt], RendererProtocol]
) -> MarkdownIt:
    """Return a Markdown parser with the required MyST configuration."""
    pass
