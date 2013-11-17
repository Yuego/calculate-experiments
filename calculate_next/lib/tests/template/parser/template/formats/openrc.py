#coding: utf-8
from __future__ import unicode_literals, absolute_import

from unittest import TestCase

from calculate_next.lib.template.parser.template.formats import OpenRCFormatParser
from ._mixin import ParserTestMixin


class TestOpenRCFormatParser(ParserTestMixin, TestCase):
    p = OpenRCFormatParser()
    basename = 'openrc'
    extension = 'conf'

    files = (
        'rc',
    )
