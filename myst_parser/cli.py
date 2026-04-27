import argparse
import sys

from markdown_it.renderer import RendererHTML
from markdown_it.rules_core import StateCore
from mdit_py_plugins.anchors import anchors_plugin

from myst_parser.config.main import MdParserConfig
from myst_parser.parsers.mdit import create_md_parser


def print_anchors(args=None):
    """ """
    pass
