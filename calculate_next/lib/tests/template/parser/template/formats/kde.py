#coding: utf-8
from __future__ import unicode_literals, absolute_import

from unittest import TestCase

from calculate_next.lib.template.parser.template.formats import KDEFormatParser
from ._mixin import ParserTestMixin


class TestKDEFormatParser(ParserTestMixin, TestCase):
    p = KDEFormatParser()
    basename = 'kde'
    extension = ''

    files = (
        'kdmrc',
    )

    merge_files = ()
