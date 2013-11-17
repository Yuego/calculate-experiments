#coding: utf-8
from __future__ import unicode_literals, absolute_import

from unittest import TestCase

from calculate_next.lib.template.parser.template.formats import PlasmaFormatParser
from ._mixin import ParserTestMixin


class TestPlasmaFormatParser(ParserTestMixin, TestCase):
    p = PlasmaFormatParser()
    basename = 'plasma'
    extension = 'ini'

    files = (
        'plasma_simple',
        'plasma',
    )
