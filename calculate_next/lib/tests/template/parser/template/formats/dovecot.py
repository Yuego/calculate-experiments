#coding: utf-8
from __future__ import unicode_literals, absolute_import

from unittest import TestCase

from calculate_next.lib.template.parser.template.formats import DovecotFormatParser
from ._mixin import ParserTestMixin


class TestDovecotFormatParser(ParserTestMixin, TestCase):
    p = DovecotFormatParser()
    basename = 'dovecot'
    extension = 'conf'

    files = (
        'example',
    )
