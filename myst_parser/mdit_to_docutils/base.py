"""Convert Markdown-it tokens to docutils nodes."""

from __future__ import annotations

import inspect
import json
import os
import posixpath
import re
from collections.abc import Callable, Iterable, Iterator, MutableMapping, Sequence
from contextlib import contextmanager, suppress
from datetime import date, datetime
from types import ModuleType
from typing import (
    TYPE_CHECKING,
    Any,
    cast,
)
from urllib.parse import urlparse

import jinja2
import yaml
from docutils import nodes
from docutils.frontend import get_default_settings
from docutils.languages import get_language
from docutils.parsers.rst import Directive, DirectiveError, directives, roles
from docutils.parsers.rst import Parser as RSTParser
from docutils.parsers.rst.directives.misc import Include
from docutils.parsers.rst.languages import get_language as get_language_rst
from docutils.statemachine import StringList
from docutils.utils import Reporter, SystemMessage, new_document
from docutils.utils.code_analyzer import Lexer, LexerError, NumberLines
from markdown_it import MarkdownIt
from markdown_it.common.utils import escapeHtml
from markdown_it.renderer import RendererProtocol
from markdown_it.token import Token
from markdown_it.tree import SyntaxTreeNode

from myst_parser import inventory
from myst_parser._compat import findall
from myst_parser.config.main import MdParserConfig, UrlSchemeType
from myst_parser.mocking import (
    MockIncludeDirective,
    MockingError,
    MockInliner,
    MockRSTParser,
    MockState,
    MockStateMachine,
)
from myst_parser.parsers.directives import MarkupError, parse_directive_text
from myst_parser.warnings_ import MystWarnings, create_warning

from .html_to_nodes import html_to_nodes

if TYPE_CHECKING:
    from sphinx.environment import BuildEnvironment


def make_document(source_path="notset", parser_cls=RSTParser) -> nodes.document:
    """Create a new docutils document, with the parser classes' default settings."""
    pass


REGEX_SCHEME = re.compile(r"^([a-zA-Z][a-zA-Z0-9+.-]*):")
"""RFC 7595: A non-empty scheme component followed by a colon (:),
consisting of a sequence of characters beginning with a letter
and followed by any combination of letters, digits, plus (+), period (.), or hyphen (-).
Although schemes are case-insensitive, the canonical form is lowercase
and documents that specify schemes must do so with lowercase letters.
"""
REGEX_URI_TEMPLATE = re.compile(
    r"{{\s*(uri|scheme|netloc|path|params|query|fragment)\s*}}"
)
REGEX_DIRECTIVE_START = re.compile(r"^[\s]{0,3}([`]{3,10}|[~]{3,10}|[:]{3,10})\{")


def token_line(token: SyntaxTreeNode, default: int | None = None) -> int:
    """Retrieve the initial line of a token."""
    pass


class DocutilsRenderer(RendererProtocol):
    """A markdown-it-py renderer to populate (in-place) a `docutils.document` AST.

    Note, this render is not dependent on Sphinx.
    """

    __output__ = "docutils"

    def __init__(self, parser: MarkdownIt) -> None:
        """Load the renderer (called by ``MarkdownIt``)"""
        self.md = parser
        self.rules = {
            k: v
            for k, v in inspect.getmembers(self, predicate=inspect.ismethod)
            if k.startswith("render_") and k != "render_children"
        }
        # these are lazy loaded, when needed
        self._inventories: None | dict[str, inventory.InventoryType] = None

    def __getattr__(self, name: str):
        """Warn when the renderer has not been setup yet."""
        if name in (
            "md_env",
            "md_config",
            "md_options",
            "document",
            "current_node",
            "reporter",
            "language_module_rst",
            "_heading_offset",
            "_level_to_section",
        ):
            raise AttributeError(
                f"'{name}' attribute is not available until setup_render() is called"
            )
        raise AttributeError(
            f"'{type(self).__name__}' object has no attribute '{name}'"
        )

    def setup_render(
        self, options: dict[str, Any], env: MutableMapping[str, Any]
    ) -> None:
        """Setup the renderer with per render variables."""
        pass

    @property
    def sphinx_env(self) -> BuildEnvironment | None:
        """Return the sphinx env, if using Sphinx."""
        pass

    def create_warning(
        self,
        message: str,
        subtype: MystWarnings | str,
        *,
        wtype: str | None = None,
        line: int | None = None,
        append_to: nodes.Element | None = None,
    ) -> nodes.system_message | None:
        """Generate a warning, logging if it is necessary.

        If the warning type is listed in the ``suppress_warnings`` configuration,
        then ``None`` will be returned and no warning logged.
        """
        pass

    def _render_tokens(self, tokens: list[Token]) -> None:
        """Render the tokens."""
        pass

    def render(
        self, tokens: Sequence[Token], options, md_env: MutableMapping[str, Any]
    ) -> nodes.document:
        """Run the render on a token stream.

        :param tokens: list on block tokens to render
        :param options: params of parser instance
        :param md_env: the markdown-it environment sandbox associated with the tokens,
            containing additional metadata like reference info
        """
        pass

    def _render_initialise(self) -> None:
        """Initialise the render of the document."""
        pass

    def _render_finalise(self) -> None:
        """Finalise the render of the document."""
        pass

    def nested_render_text(
        self,
        text: str,
        lineno: int,
        inline: bool = False,
        temp_root_node: None | nodes.Element = None,
        heading_offset: int = 0,
    ) -> None:
        """Render unparsed text (appending to the current node).

        :param text: the text to render
        :param lineno: the starting line number of the text, within the full source
        :param inline: whether the text is inline or block
        :param temp_root_node: If set, allow sections to be created as children of this node
        :param heading_offset: offset heading levels by this amount
        """
        pass

    @contextmanager
    def current_node_context(
        self, node: nodes.Element, append: bool = False
    ) -> Iterator[None]:
        """Context manager for temporarily setting the current node."""
        pass

    def render_children(self, token: SyntaxTreeNode) -> None:
        """Render the children of a token."""
        pass

    def add_line_and_source_path(self, node, token: SyntaxTreeNode) -> None:
        """Copy the line number and document source path to the docutils node."""
        pass

    def add_line_and_source_path_r(
        self, nodes_: list[nodes.Element], token: SyntaxTreeNode
    ) -> None:
        """Copy the line number and document source path to the docutils nodes,
        and recursively to all descendants.
        """
        pass

    def copy_attributes(
        self,
        token: SyntaxTreeNode,
        node: nodes.Element,
        keys: Sequence[str] = ("class",),
        *,
        converters: dict[str, Callable[[str], Any]] | None = None,
        aliases: dict[str, str] | None = None,
    ) -> None:
        """Copy attributes on the token to the docutils node.

        :param token: the token to copy attributes from
        :param node: the node to copy attributes to
        :param keys: the keys to copy from the token (after aliasing)
        :param converters: a dictionary of converters for the attributes
        :param aliases: a dictionary mapping the token key name to the node key name
        """
        pass

    def update_section_level_state(self, section: nodes.section, level: int) -> None:
        """Update the section level state, with the new current section and level."""
        pass

    def renderInlineAsText(self, tokens: list[SyntaxTreeNode]) -> str:  # noqa: N802
        """Special kludge for image `alt` attributes to conform CommonMark spec.

        Don't try to use it! Spec requires to show `alt` content with stripped markup,
        instead of simple escaping.
        """
        pass

    # ### render methods for commonmark tokens

    def render_paragraph(self, token: SyntaxTreeNode) -> None:
        pass

    def render_inline(self, token: SyntaxTreeNode) -> None:
        pass

    def render_text(self, token: SyntaxTreeNode) -> None:
        pass

    def render_bullet_list(self, token: SyntaxTreeNode) -> None:
        pass

    def render_ordered_list(self, token: SyntaxTreeNode) -> None:
        pass

    def render_list_item(self, token: SyntaxTreeNode) -> None:
        pass

    def render_em(self, token: SyntaxTreeNode) -> None:
        pass

    def render_softbreak(self, token: SyntaxTreeNode) -> None:
        pass

    def render_hardbreak(self, token: SyntaxTreeNode) -> None:
        pass

    def render_strong(self, token: SyntaxTreeNode) -> None:
        pass

    def render_blockquote(self, token: SyntaxTreeNode) -> None:
        pass

    def render_hr(self, token: SyntaxTreeNode) -> None:
        pass

    def render_code_inline(self, token: SyntaxTreeNode) -> None:
        pass

    @staticmethod
    def _parse_linenos(emphasize_lines: str, num_lines: int) -> list[int]:
        """Parse the `emphasize_lines` argument.

        Raises ValueError if the argument is invalid.
        """
        pass

    def create_highlighted_code_block(
        self,
        text: str,
        lexer_name: str | None,
        number_lines: bool = False,
        lineno_start: int = 1,
        source: str | None = None,
        line: int | None = None,
        node_cls: type[nodes.Element] = nodes.literal_block,
        emphasize_lines: list[int] | str | None = None,
    ) -> nodes.Element:
        """Create a literal block with syntax highlighting.

        This mimics the behaviour of the `code-block` directive.

        In docutils, this directive directly parses the text with the pygments lexer,
        whereas in sphinx, the lexer name is only recorded as the `language` attribute,
        and the text is lexed later by pygments within the `visit_literal_block`
        method of the output format ``SphinxTranslator``.

        Note, this function does not add the literal block to the document.
        """
        pass

    def render_code_block(self, token: SyntaxTreeNode) -> None:
        pass

    def render_fence(self, token: SyntaxTreeNode) -> None:
        """Render a fenced code block."""
        pass

    @property
    def blocks_mathjax_processing(self) -> bool:
        """Only add mathjax ignore classes if using sphinx,
        and using the ``dollarmath`` extension, and ``myst_update_mathjax=True``.
        """
        pass

    def generate_heading_target(
        self,
        token: SyntaxTreeNode,
        level: int,
        node: nodes.Element,
        title_node: nodes.Element,
    ) -> None:
        """Generate a heading target, and add it to the document."""
        pass

    def render_heading(self, token: SyntaxTreeNode) -> None:
        """Render a heading, e.g. `# Heading`."""
        pass

    def render_link(self, token: SyntaxTreeNode) -> None:
        """Parse `<http://link.com>` or `[text](link "title")` syntax to docutils AST:

        - If `myst_all_links_external` is True, forward to `render_link_url`
        - If the link token has a class attribute containing `external`,
            forward to `render_link_url`
        - If the link is an id link (e.g. `#id`), forward to `render_link_anchor`
        - If the link has a schema, and the schema is in `url_schemes` (e.g. `http:`),
          forward to `render_link_url`
        - If the link has an `inv:` schema, forward to `render_link_inventory`
        - If the link is an autolink/linkify type link, forward to `render_link_url`
        - Otherwise, forward to `render_link_internal`
        """
        pass

    def render_link_url(
        self, token: SyntaxTreeNode, conversion: None | UrlSchemeType = None
    ) -> None:
        """Render link token (including autolink and linkify),
        where the link has been identified as an external URL.
        """
        pass

    def render_link_path(self, token: SyntaxTreeNode) -> None:
        """Render a link token like `<path:...>`."""
        pass

    def render_link_project(self, token: SyntaxTreeNode) -> None:
        """Render a link token like `<project:...>`."""
        pass

    def render_link_anchor(self, token: SyntaxTreeNode, target: str) -> None:
        """Render link token like `[text](#target)`, to a local target.

        :target: the target id, e.g. `#target`
        """
        pass

    def render_link_unknown(self, token: SyntaxTreeNode) -> None:
        """Render link token `[text](link "title")`,
        where the link has not been identified as an external URL::

            <reference refname="link" title="title">
                text

        `text` can contain nested syntax, e.g. `[**bold**](link "title")`.

        Note, this is overridden by `SphinxRenderer`, to use `pending_xref` nodes.
        """
        pass

    def render_link_inventory(self, token: SyntaxTreeNode) -> None:
        r"""Create a link to an inventory object.

        This assumes the href is of the form `<scheme>:<path>#<target>`.
        The path is of the form `<invs>:<domains>:<otypes>`,
        where each of the parts is optional, hence `<scheme>:#<target>` is also valid.
        Each of the path parts can contain the `*` wildcard, for example:
        `<scheme>:key:*:obj#targe*`.
        `\*` is treated as a plain `*`.
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
        """Return inventory matches.

        This will be overridden for sphinx, to use intersphinx config.
        """
        pass

    def render_html_inline(self, token: SyntaxTreeNode) -> None:
        pass

    def render_html_block(self, token: SyntaxTreeNode) -> None:
        pass

    def render_image(self, token: SyntaxTreeNode) -> None:
        pass

    # ### render methods for plugin tokens

    def render_span(self, token: SyntaxTreeNode) -> None:
        """Render an inline span token."""
        pass

    def render_front_matter(self, token: SyntaxTreeNode) -> None:
        """Pass document front matter data."""
        pass

    def dict_to_fm_field_list(
        self, data: dict[str, Any], language_code: str, line: int = 0
    ) -> nodes.field_list:
        """Render each key/val pair as a docutils ``field_node``.

        Bibliographic keys below will be parsed as Markdown,
        all others will be left as literal text.

        The field list should be at the start of the document,
        and will then be converted to a `docinfo` node during the
        `docutils.docutils.transforms.frontmatter.DocInfo` transform (priority 340),
        and bibliographic keys (or their translation) will be converted to nodes::

            {'author': docutils.nodes.author,
            'authors': docutils.nodes.authors,
            'organization': docutils.nodes.organization,
            'address': docutils.nodes.address,
            'contact': docutils.nodes.contact,
            'version': docutils.nodes.version,
            'revision': docutils.nodes.revision,
            'status': docutils.nodes.status,
            'date': docutils.nodes.date,
            'copyright': docutils.nodes.copyright,
            'dedication': docutils.nodes.topic,
            'abstract': docutils.nodes.topic}

        Also, the 'dedication' and 'abstract' will be placed outside the `docinfo`,
        and so will always be shown in the document.

        If using sphinx, this `docinfo` node will later be extracted from the AST,
        by the `DoctreeReadEvent` transform (priority 880),
        calling `MetadataCollector.process_doc`.
        In this case keys and values will be converted to strings and stored in
        `app.env.metadata[app.env.docname]`

        See
        https://www.sphinx-doc.org/en/master/usage/restructuredtext/field-lists.html
        for docinfo fields used by sphinx.

        """
        pass

    def render_table(self, token: SyntaxTreeNode) -> None:
        # markdown-it table always contains at least a header:
        pass

    def render_table_row(self, token: SyntaxTreeNode) -> None:
        pass

    def render_s(self, token: SyntaxTreeNode) -> None:
        """Render a strikethrough token."""
        pass

    def render_math_inline(self, token: SyntaxTreeNode) -> None:
        pass

    def render_math_inline_double(self, token: SyntaxTreeNode) -> None:
        pass

    def render_math_single(self, token: SyntaxTreeNode) -> None:
        pass

    def render_math_block(self, token: SyntaxTreeNode) -> None:
        pass

    def render_math_block_label(self, token: SyntaxTreeNode) -> None:
        pass

    def render_amsmath(self, token: SyntaxTreeNode) -> None:
        # note docutils does not currently support the nowrap attribute
        # or equation numbering, so this is overridden in the sphinx renderer
        pass

    def render_footnote_ref(self, token: SyntaxTreeNode) -> None:
        """Footnote references are added as auto-numbered,
        .i.e. `[^a]` is read as rST `[#a]_`
        """
        pass

    def render_footnote_reference(self, token: SyntaxTreeNode) -> None:
        """Despite the name, this is actually a footnote definition, e.g. `[^a]: ...`"""
        pass

    def render_myst_block_break(self, token: SyntaxTreeNode) -> None:
        pass

    def render_myst_target(self, token: SyntaxTreeNode) -> None:
        pass

    def render_myst_line_comment(self, token: SyntaxTreeNode) -> None:
        pass

    def render_myst_role(self, token: SyntaxTreeNode) -> None:
        pass

    def render_colon_fence(self, token: SyntaxTreeNode) -> None:
        """Render a div block, with ``:`` colon delimiters."""
        pass

    def render_dl(self, token: SyntaxTreeNode) -> None:
        """Render a definition list."""
        pass

    def render_field_list(self, token: SyntaxTreeNode) -> None:
        """Render a field list."""
        pass

    def render_restructuredtext(self, token: SyntaxTreeNode) -> None:
        """Render the content of the token as restructuredtext."""
        pass

    def render_directive(
        self,
        token: SyntaxTreeNode,
        name: str,
        arguments: str,
        *,
        additional_options: dict[str, str] | None = None,
    ) -> None:
        """Render special fenced code blocks as directives.

        :param token: the token to render
        :param name: the name of the directive
        :param arguments: The remaining text on the same line as the directive name.
        """
        pass

    def run_directive(
        self,
        name: str,
        first_line: str,
        content: str,
        position: int,
        additional_options: dict[str, str] | None = None,
    ) -> list[nodes.Element]:
        """Run a directive and return the generated nodes.

        :param name: the name of the directive
        :param first_line: The text on the same line as the directive name.
            May be an argument or body text, dependent on the directive
        :param content: All text after the first line. Can include options.
        :param position: The line number of the first line
        :param additional_options: Additional options to add to the directive,
            above those parsed from the content.

        """
        pass

    def render_substitution_inline(self, token: SyntaxTreeNode) -> None:
        """Render inline substitution {{key}}."""
        pass

    def render_substitution_block(self, token: SyntaxTreeNode) -> None:
        """Render block substitution {{key}}."""
        pass

    def render_substitution(self, token: SyntaxTreeNode, inline: bool) -> None:
        """Substitutions are rendered by:

        1. Combining global substitutions with front-matter substitutions
           to create a variable context (front-matter takes priority)
        2. Add the sphinx `env` to the variable context (if available)
        3. Create the string content with Jinja2 (passing it the variable context)
        4. If the substitution is inline and not a directive,
           parse to nodes ignoring block syntaxes (like lists or block-quotes),
           otherwise parse to nodes with all syntax rules.

        """
        pass


def html_meta_to_nodes(
    data: dict[str, Any], document: nodes.document, line: int, reporter: Reporter
) -> list[nodes.meta | nodes.system_message]:
    """Replicate the `meta` directive,
    by converting a dictionary to a list of pending meta nodes

    See:
    https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html#html-metadata
    """
    pass


def clean_astext(node: nodes.Element) -> str:
    """Like node.astext(), but ignore images.
    Copied from sphinx.
    """
    pass


_SLUGIFY_CLEAN_REGEX = re.compile(r"[^\w\u4e00-\u9fff\- ]")


def default_slugify(title: str) -> str:
    """Default slugify function.

    This aims to mimic the GitHub Markdown format, see:

    - https://github.com/jch/html-pipeline/blob/master/lib/html/pipeline/toc_filter.rb
    - https://gist.github.com/asabaylus/3071099
    """
    pass


def compute_unique_slug(
    token_tree: SyntaxTreeNode,
    slugs: Iterable[str],
    slug_func: None | Callable[[str], str] = None,
) -> str:
    """Compute the slug for a token.

    This directly mirrors the logic in `mdit_py_plugins.anchors_plugin`
    """
    pass
