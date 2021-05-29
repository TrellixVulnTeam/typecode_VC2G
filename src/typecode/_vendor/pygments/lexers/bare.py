# -*- coding: utf-8 -*-
"""
    pygments.lexers.bare
    ~~~~~~~~~~~~~~~~~~~~

    Lexer for the BARE schema.

    :copyright: Copyright 2006-2021 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import re

from typecode._vendor.pygments.lexer import RegexLexer, words, bygroups
from typecode._vendor.pygments.token import Text, Comment, Keyword, Name, Literal

__all__ = ['BareLexer']


class BareLexer(RegexLexer):
    """
    For `BARE schema <https://baremessages.org>`_ schema source.

    .. versionadded:: 2.7
    """
    name = 'BARE'
    filenames = ['*.bare']
    aliases = ['bare']

    flags = re.MULTILINE | re.UNICODE

    keywords = [
        'type',
        'enum',
        'u8',
        'u16',
        'u32',
        'u64',
        'uint',
        'i8',
        'i16',
        'i32',
        'i64',
        'int',
        'f32',
        'f64',
        'bool',
        'void',
        'data',
        'string',
        'optional',
        'map',
    ]

    tokens = {
        'root': [
            (r'(type)(\s+)([A-Z][a-zA-Z0-9]+)(\s+\{)',
             bygroups(Keyword, Text, Name.Class, Text), 'struct'),
            (r'(type)(\s+)([A-Z][a-zA-Z0-9]+)(\s+\()',
             bygroups(Keyword, Text, Name.Class, Text), 'union'),
            (r'(type)(\s+)([A-Z][a-zA-Z0-9]+)(\s+)',
             bygroups(Keyword, Text, Name, Text), 'typedef'),
            (r'(enum)(\s+)([A-Z][a-zA-Z0-9]+)(\s+\{)',
             bygroups(Keyword, Text, Name.Class, Text), 'enum'),
            (r'#.*?$', Comment),
            (r'\s+', Text),
        ],
        'struct': [
            (r'\{', Text, '#push'),
            (r'\}', Text, '#pop'),
            (r'([a-zA-Z0-9]+)(:\s*)', bygroups(Name.Attribute, Text), 'typedef'),
            (r'\s+', Text),
        ],
        'union': [
            (r'\)', Text, '#pop'),
            (r'\s*\|\s*', Text),
            (r'[A-Z][a-zA-Z0-9]+', Name.Class),
            (words(keywords), Keyword),
            (r'\s+', Text),
        ],
        'typedef': [
            (r'\[\]', Text),
            (r'#.*?$', Comment, '#pop'),
            (r'(\[)(\d+)(\])', bygroups(Text, Literal, Text)),
            (r'<|>', Text),
            (r'\(', Text, 'union'),
            (r'(\[)([a-z][a-z-A-Z0-9]+)(\])', bygroups(Text, Keyword, Text)),
            (r'(\[)([A-Z][a-z-A-Z0-9]+)(\])', bygroups(Text, Name.Class, Text)),
            (r'([A-Z][a-z-A-Z0-9]+)', Name.Class),
            (words(keywords), Keyword),
            (r'\n', Text, '#pop'),
            (r'\{', Text, 'struct'),
            (r'\s+', Text),
            (r'\d+', Literal),
        ],
        'enum': [
            (r'\{', Text, '#push'),
            (r'\}', Text, '#pop'),
            (r'([A-Z][A-Z0-9_]*)(\s*=\s*)(\d+)', bygroups(Name.Attribute, Text, Literal)),
            (r'([A-Z][A-Z0-9_]*)', bygroups(Name.Attribute)),
            (r'#.*?$', Comment),
            (r'\s+', Text),
        ],
    }
