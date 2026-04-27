"""Parser for directive options.

This is a highly restricted parser for YAML,
which only allows a subset of YAML to be used for directive options:

- Only block mappings are allowed at the top level
- Mapping keys are parsed as strings (plain or quoted)
- Mapping values are parsed as strings (plain, quoted, literal `|`, folded `>`)
- `#` Comments are allowed and blank lines

Adapted from:
https://github.com/yaml/pyyaml/commit/957ae4d495cf8fcb5475c6c2f1bce801096b68a5

For a good description of multi-line YAML strings, see:
https://stackoverflow.com/a/21699210/5033292
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, replace
from typing import ClassVar, Final, Literal, cast


@dataclass
class Position:
    """Position of a character in a stream."""

    index: int
    line: int
    column: int


class StreamBuffer:
    """A buffer for a stream of characters."""

    def __init__(self, stream: str):
        self._buffer = stream + _CHARS_END
        self._index = 0
        self._line = 0
        self._column = 0

    @property
    def index(self) -> int:
        pass

    @property
    def line(self) -> int:
        pass

    @property
    def column(self) -> int:
        pass

    def peek(self, index: int = 0) -> str:
        pass

    def prefix(self, length: int = 1) -> str:
        pass

    def forward(self, length: int = 1) -> None:
        pass

    def get_position(self) -> Position:
        pass


@dataclass
class Token:
    """A parsed token from a directive option stream."""

    id: ClassVar[str] = "<unknown>"
    start: Position
    end: Position


@dataclass
class KeyToken(Token):
    id: ClassVar[str] = "<key>"
    value: str
    style: Literal[None, "'", '"'] = None
    """The original style of the string."""


@dataclass
class ValueToken(Token):
    id: ClassVar[str] = "<value>"
    value: str
    style: Literal[None, "'", '"', "|", ">"] = None
    """The original style of the string."""


@dataclass
class ColonToken(Token):
    id: ClassVar[str] = "<colon>"


class TokenizeError(Exception):
    def __init__(
        self,
        problem: str,
        problem_mark: Position,
        context: str | None = None,
        context_mark: Position | None = None,
    ):
        """A YAML error with optional context.

        :param problem: The problem encountered
        :param problem_mark: The position of the problem
        :param context: The context of the error, e.g. the parent being scanned
        :param context_mark: The position of the context
        """
        self.context = context
        self.context_mark = context_mark
        self.problem = problem
        self.problem_mark = problem_mark

    def clone(self, line_offset: int, column_offset: int) -> TokenizeError:
        """Clone the error with the given line and column offsets."""
        pass

    def __str__(self) -> str:
        lines = []
        if self.context is not None:
            lines.append(self.context)
        if self.context_mark is not None and (
            self.context_mark.line != self.problem_mark.line
            or self.context_mark.column != self.problem_mark.column
        ):
            lines.append(
                f"at line {self.context_mark.line}, column {self.context_mark.column}"
            )
        if self.problem is not None:
            lines.append(self.problem)
        if self.problem_mark is not None:
            lines.append(
                f"at line {self.problem_mark.line}, column {self.problem_mark.column}"
            )
        return "\n".join(lines)


@dataclass
class State:
    has_comments: bool = False


def options_to_items(
    text: str, line_offset: int = 0, column_offset: int = 0
) -> tuple[list[tuple[str, str]], State]:
    """Parse a directive option block into (key, value) tuples.

    :param text: The directive option text.
    :param line_offset: The line offset to apply to the error positions.
    :param column_offset: The column offset to apply to the error positions.

    :raises: `TokenizeError`
    """
    pass


def _to_tokens(
    text: str, state: State, line_offset: int = 0, column_offset: int = 0
) -> Iterable[tuple[KeyToken, ValueToken | None]]:
    """Parse a directive option, and yield key/value token pairs.

    :param text: The directive option text.
    :param line_offset: The line offset to apply to the error positions.
    :param column_offset: The column offset to apply to the error positions.

    :raises: `TokenizeError`
    """
    pass


def _tokenize(text: str, state: State) -> Iterable[Token]:
    """Yield tokens from a directive option stream."""
    pass


def _scan_to_next_token(stream: StreamBuffer, state: State) -> None:
    """Skip spaces, line breaks and comments.

    The byte order mark is also stripped,
    if it's the first character in the stream.
    """
    pass


def _scan_plain_scalar(
    stream: StreamBuffer, state: State, is_key: bool = False
) -> KeyToken | ValueToken:
    pass


def _scan_plain_spaces(stream: StreamBuffer, allow_newline: bool = True) -> list[str]:
    pass


def _scan_line_break(stream: StreamBuffer) -> str:
    # Transforms:
    #   '\r\n'      :   '\n'
    #   '\r'        :   '\n'
    #   '\n'        :   '\n'
    #   '\x85'      :   '\n'
    #   '\u2028'    :   '\u2028'
    #   '\u2029     :   '\u2029'
    #   default     :   ''
    pass


def _scan_flow_scalar(
    stream: StreamBuffer, style: Literal["'", '"'], is_key: bool = False
) -> KeyToken | ValueToken:
    pass


def _scan_flow_scalar_non_spaces(
    stream: StreamBuffer, double: bool, start_mark: Position
) -> list[str]:
    pass


def _scan_flow_scalar_spaces(stream: StreamBuffer, start_mark: Position) -> list[str]:
    pass


def _scan_flow_scalar_breaks(stream: StreamBuffer) -> list[str]:
    pass


def _scan_block_scalar(
    stream: StreamBuffer, style: Literal["|", ">"], state: State
) -> ValueToken:
    pass


def _scan_block_scalar_indicators(
    stream: StreamBuffer, start_mark: Position
) -> tuple[bool | None, int | None]:
    pass


def _scan_block_scalar_ignored_line(
    stream: StreamBuffer, start_mark: Position, state: State
) -> None:
    pass


def _scan_block_scalar_indentation(
    stream: StreamBuffer,
) -> tuple[list[str], int, Position]:
    pass


def _scan_block_scalar_breaks(
    stream: StreamBuffer, indent: int
) -> tuple[list[str], Position]:
    pass


_CHARS_END: Final[str] = "\0"
_CHARS_NEWLINE: Final[str] = "\r\n\x85\u2028\u2029"
_CHARS_END_NEWLINE: Final[str] = "\0\r\n\x85\u2028\u2029"
_CHARS_SPACE_NEWLINE: Final[str] = " \r\n\x85\u2028\u2029"
_CHARS_END_SPACE_NEWLINE: Final[str] = "\0 \r\n\x85\u2028\u2029"
_CHARS_END_SPACE_TAB_NEWLINE: Final[str] = "\0 \t\r\n\x85\u2028\u2029"

_ESCAPE_REPLACEMENTS: Final[dict[str, str]] = {
    "0": "\0",
    "a": "\x07",
    "b": "\x08",
    "t": "\x09",
    "\t": "\x09",
    "n": "\x0a",
    "v": "\x0b",
    "f": "\x0c",
    "r": "\x0d",
    "e": "\x1b",
    " ": "\x20",
    '"': '"',
    "\\": "\\",
    "/": "/",
    "N": "\x85",
    "_": "\xa0",
    "L": "\u2028",
    "P": "\u2029",
}

_ESCAPE_CODES: Final[dict[str, int]] = {
    "x": 2,
    "u": 4,
    "U": 8,
}
