#coding: utf-8
from __future__ import unicode_literals, absolute_import

from unittest import TestCase

from calculate_next.lib.template.parser.template.formats import BindFormatParser
from ._mixin import ParserTestMixin


class TestBindFormatParser(ParserTestMixin, TestCase):
    p = BindFormatParser()
    basename = 'named'
    extension = 'conf'

    files = (
        'named_simple',
        'named',
    )
