#coding: utf-8
from __future__ import unicode_literals, absolute_import

import codecs
from collections import OrderedDict
from unittest import TestCase

from calculate_next.lib.template.parser.template.formats.dhcp import DHCPFormatParser

from ._mixin import ParserTestMixin


class TestDHCPFormatParser(TestCase):
    p = DHCPFormatParser()
    files = (
        './data/tests/configs/dhcpd.conf',
    )


