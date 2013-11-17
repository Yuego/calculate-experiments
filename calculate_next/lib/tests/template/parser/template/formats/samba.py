#coding: utf-8
from __future__ import unicode_literals, absolute_import

from unittest import TestCase

from calculate_next.lib.template.parser.template.formats import SambaFormatParser
from ._mixin import ParserTestMixin


class TestSambaFormatParser(ParserTestMixin, TestCase):
    p = SambaFormatParser()
    basename = 'smb'
    extension = 'conf'

    files = (
        'smb',
    )

    merge_files = (
        'merge',
    )
