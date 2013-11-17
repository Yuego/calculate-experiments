#coding: utf-8
from __future__ import unicode_literals, absolute_import

from unittest import TestCase

from calculate_next.lib.template.parser.template.formats import SquidFormatParser
from ._mixin import ParserTestMixin

class TestSquidFormatParser(ParserTestMixin, TestCase):
    p = SquidFormatParser()
    basename = 'squid'
    extension = 'conf'

    files = (
        'calomel.org',
    )

    merge_files = ()

