#coding: utf-8
from __future__ import unicode_literals, absolute_import

import codecs
from collections import OrderedDict
from unittest import TestCase

from calculate_next.lib.template.parser.template.formats.bind import BindFormatParser

from ._mixin import ParserTestMixin


class TestBindFormatParser(ParserTestMixin, TestCase):
    p = BindFormatParser()
    files = (
        #'./data/tests/configs/named_simple.conf',
        './data/tests/configs/named.conf',
    )

    def test_parser(self):
        syntax = self.p.get_original_syntax()

        first_content = self._open_file(self.files[0])
        first_result = syntax.parseString(first_content, parseAll=True)
        first_tree = self.p.expand_tree(first_result)

        #print first_tree

