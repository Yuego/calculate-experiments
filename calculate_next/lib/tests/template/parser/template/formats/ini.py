#coding: utf-8
from __future__ import unicode_literals, absolute_import

from unittest import TestCase

from calculate_next.lib.template.parser.template.formats import INIFormatParser
from ._mixin import ParserTestMixin

class TestINIFormatParser(ParserTestMixin, TestCase):
    p = INIFormatParser()
    basename = 'ini'
    extension = 'ini'

    files = (
        'ini_simple',
    )

