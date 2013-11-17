#coding: utf-8
from __future__ import unicode_literals, absolute_import

from unittest import TestCase

from calculate_next.lib.template.parser.template.formats import WorldFormatParser
from ._mixin import ParserTestMixin

class TestINIFormatParser(ParserTestMixin, TestCase):
    p = WorldFormatParser()
    basename = 'world'
    extension = ''

    files = (
        'world',
    )

