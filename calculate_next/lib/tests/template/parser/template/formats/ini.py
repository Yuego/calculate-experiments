#coding: utf-8
from __future__ import unicode_literals, absolute_import

from collections import OrderedDict
from unittest import TestCase

from calculate_next.lib.template.parser.template.formats.ini import INIFormatParser

from ._mixin import ParserTestMixin

class TestINIFormatParser(ParserTestMixin, TestCase):
    p = INIFormatParser()
    files = (
        './data/tests/configs/simple.ini',
    )

