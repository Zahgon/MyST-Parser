"""The configuration for the myst parser."""

import dataclasses as dc
from collections.abc import Callable, Iterable, Iterator, Sequence
from importlib import import_module
from typing import (
    Any,
    TypedDict,
)

from myst_parser.warnings_ import MystWarnings

from .dc_validators import (
    any_,
    deep_iterable,
    deep_mapping,
    in_,
    instance_of,
    optional,
    validate_field,
    validate_fields,
)


def check_extensions(inst: "MdParserConfig", field: dc.Field, value: Any) -> None:
    """Check that the extensions are a list of known strings"""
    pass


class UrlSchemeType(TypedDict, total=False):
    """Type of the external schemes dictionary."""

    url: str
    title: str
    classes: list[str]


def check_url_schemes(inst: "MdParserConfig", field: dc.Field, value: Any) -> None:
    """Check that the external schemes are of the right format."""
    pass


def check_sub_delimiters(_: "MdParserConfig", field: dc.Field, value: Any) -> None:
    """Check that the sub_delimiters are a tuple of length 2 of strings of length 1"""
    pass


def check_inventories(_: "MdParserConfig", field: dc.Field, value: Any) -> None:
    """Check that the inventories are a dict of {str: (str, Optional[str])}"""
    pass


def check_heading_slug_func(
    inst: "MdParserConfig", field: dc.Field, value: Any
) -> None:
    """Check that the heading_slug_func is a callable."""
    pass


def _test_slug_func(text: str) -> str:
    """Dummy slug function, this is imported during testing."""
    pass


def check_fence_as_directive(
    inst: "MdParserConfig", field: dc.Field, value: Any
) -> None:
    """Check that the extensions are a sequence of known strings"""
    pass


@dc.dataclass()
class MdParserConfig:
    """Configuration options for the Markdown Parser.

    Note in the sphinx configuration these option names are prepended with ``myst_``
    """

    def __repr__(self) -> str:
        """Return a string representation of the config."""
        # this replicates the auto-generated __repr__,
        # but also allows for a repr function to be defined on the field
        attributes: list[str] = []
        for name, val, f in self.as_triple():
            if not f.repr:
                continue
            val_str = f.metadata.get("repr_func", repr)(val)
            attributes.append(f"{name}={val_str}")
        return f"{self.__class__.__name__}({', '.join(attributes)})"

    # TODO replace commonmark_only, gfm_only with a single option

    commonmark_only: bool = dc.field(
        default=False,
        metadata={
            "validator": instance_of(bool),
            "help": "Use strict CommonMark parser",
        },
    )
    gfm_only: bool = dc.field(
        default=False,
        metadata={
            "validator": instance_of(bool),
            "help": "Use strict Github Flavoured Markdown parser",
        },
    )

    enable_extensions: set[str] = dc.field(
        default_factory=set,
        metadata={"validator": check_extensions, "help": "Enable syntax extensions"},
    )

    disable_syntax: Iterable[str] = dc.field(
        default_factory=list,
        metadata={
            "validator": deep_iterable(instance_of(str), instance_of((list, tuple))),
            "help": "Disable Commonmark syntax elements",
        },
    )

    all_links_external: bool = dc.field(
        default=False,
        metadata={
            "validator": instance_of(bool),
            "help": "Parse all links as simple hyperlinks",
        },
    )

    links_external_new_tab: bool = dc.field(
        default=False,
        metadata={
            "validator": instance_of(bool),
            "help": "Open all external links in a new tab",
        },
    )

    url_schemes: dict[str, UrlSchemeType | None] = dc.field(
        default_factory=lambda: {
            "http": None,
            "https": None,
            "mailto": None,
            "ftp": None,
        },
        metadata={
            "validator": check_url_schemes,
            "help": "URI schemes that are converted to external links",
            "repr_func": lambda v: repr(tuple(v)),
            # Note, lists of strings will be coerced to dicts in the validator
            "doc_type": "list[str] | dict[str, None | str | dict]",
        },
    )

    ref_domains: Iterable[str] | None = dc.field(
        default=None,
        metadata={
            "validator": optional(
                deep_iterable(instance_of(str), instance_of((list, tuple)))
            ),
            "help": "Sphinx domain names to search in for link references",
            "omit": ["docutils"],
        },
    )

    fence_as_directive: set[str] = dc.field(
        default_factory=set,
        metadata={
            "validator": check_fence_as_directive,
            "help": "Interpret a code fence as a directive, for certain language names. "
            "This can be useful for fences like dot and mermaid, "
            "and interoperability with other Markdown renderers.",
        },
    )

    number_code_blocks: Sequence[str] = dc.field(
        default_factory=list,
        metadata={
            "validator": deep_iterable(instance_of(str), instance_of((list, tuple))),
            "help": "Add line numbers to code blocks with these languages",
        },
    )

    title_to_header: bool = dc.field(
        default=False,
        metadata={
            "validator": instance_of(bool),
            "help": "Convert a `title` field in the front-matter to a H1 header",
        },
    )

    heading_anchors: int = dc.field(
        default=0,
        metadata={
            "validator": optional(in_([0, 1, 2, 3, 4, 5, 6, 7])),
            "help": "Heading level depth to assign HTML anchors",
        },
    )

    heading_slug_func: Callable[[str], str] | None = dc.field(
        default=None,
        metadata={
            "validator": check_heading_slug_func,
            "help": (
                "Function for creating heading anchors, "
                "or a python import path e.g. `my_package.my_module.my_function`"
            ),
            "global_only": True,
            "doc_type": "None | Callable[[str], str] | str",
        },
    )

    html_meta: dict[str, str] = dc.field(
        default_factory=dict,
        metadata={
            "validator": deep_mapping(
                instance_of(str), instance_of(str), instance_of(dict)
            ),
            "merge_topmatter": True,
            "help": "HTML meta tags",
            "repr_func": lambda v: f"{{{', '.join(f'{k}: ...' for k in v)}}}",
        },
    )

    footnote_sort: bool = dc.field(
        default=True,
        metadata={
            "validator": instance_of(bool),
            "help": "Move all footnotes to the end of the document, and sort by reference order",
        },
    )

    footnote_transition: bool = dc.field(
        default=True,
        metadata={
            "validator": instance_of(bool),
            "help": "Place a transition before sorted footnotes",
        },
    )

    words_per_minute: int = dc.field(
        default=200,
        metadata={
            "validator": instance_of(int),
            "help": "For reading speed calculations",
        },
    )

    # Extension specific

    substitutions: dict[str, Any] = dc.field(
        default_factory=dict,
        metadata={
            "validator": deep_mapping(instance_of(str), any_, instance_of(dict)),
            "merge_topmatter": True,
            "help": "Substitutions mapping",
            "extension": "substitutions",
            "repr_func": lambda v: f"{{{', '.join(f'{k}: ...' for k in v)}}}",
        },
    )

    sub_delimiters: tuple[str, str] = dc.field(
        default=("{", "}"),
        repr=False,
        metadata={
            "validator": check_sub_delimiters,
            "help": "Substitution delimiters",
            "extension": "substitutions",
            "omit": ["docutils"],
        },
    )

    linkify_fuzzy_links: bool = dc.field(
        default=True,
        metadata={
            "validator": instance_of(bool),
            "help": "Recognise URLs without schema prefixes",
            "extension": "linkify",
        },
    )

    dmath_allow_labels: bool = dc.field(
        default=True,
        metadata={
            "validator": instance_of(bool),
            "help": "Parse `$$...$$ (label)`",
            "extension": "dollarmath",
        },
    )
    dmath_allow_space: bool = dc.field(
        default=True,
        metadata={
            "validator": instance_of(bool),
            "help": "Allow initial/final spaces in `$ ... $`",
            "extension": "dollarmath",
        },
    )
    dmath_allow_digits: bool = dc.field(
        default=True,
        metadata={
            "validator": instance_of(bool),
            "help": "Allow initial/final digits `1$ ...$2`",
            "extension": "dollarmath",
        },
    )
    dmath_double_inline: bool = dc.field(
        default=False,
        metadata={
            "validator": instance_of(bool),
            "help": "Parse inline `$$ ... $$`",
            "extension": "dollarmath",
        },
    )

    update_mathjax: bool = dc.field(
        default=True,
        metadata={
            "validator": instance_of(bool),
            "help": "Update sphinx.ext.mathjax configuration to ignore `$` delimiters",
            "extension": "dollarmath",
            "global_only": True,
            "omit": ["docutils"],
        },
    )

    mathjax_classes: str = dc.field(
        default="tex2jax_process|mathjax_process|math|output_area",
        metadata={
            "validator": instance_of(str),
            "help": "MathJax classes to add to math HTML",
            "extension": "dollarmath",
            "global_only": True,
            "omit": ["docutils"],
        },
    )

    enable_checkboxes: bool = dc.field(
        default=False,
        metadata={
            "validator": instance_of(bool),
            "help": "Enable checkboxes",
            "extension": "tasklist",
        },
    )

    # docutils only (replicating aspects of sphinx config)

    suppress_warnings: Sequence[str] = dc.field(
        default_factory=list,
        metadata={
            "validator": deep_iterable(instance_of(str), instance_of((list, tuple))),
            "help": "A list of warning types to suppress warning messages",
            "omit": ["sphinx"],
            "global_only": True,
        },
    )

    highlight_code_blocks: bool = dc.field(
        default=True,
        metadata={
            "validator": instance_of(bool),
            "help": "Syntax highlight code blocks with pygments",
            "omit": ["sphinx"],
        },
    )

    inventories: dict[str, tuple[str, str | None]] = dc.field(
        default_factory=dict,
        repr=False,
        metadata={
            "validator": check_inventories,
            "help": "Mapping of key to (url, inv file), for intra-project referencing",
            "omit": ["sphinx"],
            "global_only": True,
        },
    )

    def __post_init__(self):
        validate_fields(self)

    def copy(self, **kwargs: Any) -> "MdParserConfig":
        """Return a new object replacing specified fields with new values.

        Note: initiating the copy will also validate the new fields.
        """
        pass

    @classmethod
    def get_fields(cls) -> tuple[dc.Field, ...]:
        """Return all attribute fields in this class."""
        return dc.fields(cls)

    def as_dict(self, dict_factory=dict) -> dict:
        """Return a dictionary of field name -> value."""
        pass

    def as_triple(self) -> Iterable[tuple[str, Any, dc.Field]]:
        """Yield triples of (name, value, field)."""
        pass


def merge_file_level(
    config: MdParserConfig,
    topmatter: dict[str, Any],
    warning: Callable[[MystWarnings, str], None],
) -> MdParserConfig:
    """Merge the file-level topmatter with the global config.

    :param config: Global config.
    :param topmatter: Topmatter from the file.
    :param warning: Function to call with a warning (type, message).
    :returns: A new config object
    """
    pass


class TopmatterReadError(Exception):
    """Topmatter parsing error."""


def read_topmatter(text: str | Iterator[str]) -> dict[str, Any] | None:
    """Read the (optional) YAML topmatter from a source string.

    This is identified by the first line starting with `---`,
    then read up to a terminating line of `---`, or `...`.

    :param source: The source string to read from
    :return: The topmatter
    """
    pass
