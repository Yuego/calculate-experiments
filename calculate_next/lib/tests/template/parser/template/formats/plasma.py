#coding: utf-8
from __future__ import unicode_literals, absolute_import

from collections import OrderedDict
from unittest import TestCase

from calculate_next.lib.template.parser.template.formats.plasma import PlasmaFormatParser

from ._mixin import ParserTestMixin


class TestPlasmaFormatParser(ParserTestMixin, TestCase):
    p = PlasmaFormatParser()
    files = (
        './data/tests/configs/plasma_simple.ini',
        './data/tests/configs/plasma.ini',
    )
