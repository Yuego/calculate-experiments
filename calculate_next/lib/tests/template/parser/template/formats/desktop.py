#coding: utf-8
from __future__ import unicode_literals, absolute_import

from unittest import TestCase

from calculate_next.lib.template.parser.template.formats import DesktopFormatParser
from ._mixin import ParserTestMixin


class TestDesktopFormatParser(ParserTestMixin, TestCase):
    p = DesktopFormatParser()
    basename = 'desktop'
    extension = 'desktop'

    files = (
        'bsh',
        'convert',
    )

    merge_files = ()
