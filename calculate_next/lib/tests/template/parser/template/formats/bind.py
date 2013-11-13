#coding: utf-8
from __future__ import unicode_literals, absolute_import

import codecs
from collections import OrderedDict
from copy import deepcopy
from unittest import TestCase

from calculate_next.lib.template.parser.template.formats.bind import BindFormatParser

from ._mixin import ParserTestMixin


class TestBindFormatParser(ParserTestMixin, TestCase):
    p = BindFormatParser()
    files = (
        './data/tests/configs/named_simple.conf',
        './data/tests/configs/named.conf',
    )

    merge_files = (
        './data/tests/configs/named_merge_dst.conf',
        './data/tests/configs/named_merge_src.conf',
        './data/tests/configs/named_merge_result.conf',
    )
