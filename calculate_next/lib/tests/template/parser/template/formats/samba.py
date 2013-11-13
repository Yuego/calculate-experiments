#coding: utf-8
from __future__ import unicode_literals, absolute_import

from collections import OrderedDict
from unittest import TestCase

from calculate_next.lib.template.parser.template.formats.samba import SambaFormatParser

from ._mixin import ParserTestMixin


class TestSambaFormatParser(ParserTestMixin, TestCase):
    p = SambaFormatParser()
    files = (
        './data/tests/configs/smb.conf',
    )

    merge_files = (
        './data/tests/configs/smb_merge_dst.conf',
        './data/tests/configs/smb_merge_src.conf',
        './data/tests/configs/smb_merge_result.conf',
    )
