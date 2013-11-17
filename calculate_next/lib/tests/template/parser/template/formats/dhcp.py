#coding: utf-8
from __future__ import unicode_literals, absolute_import

from unittest import TestCase

from calculate_next.lib.template.parser.template.formats import DHCPFormatParser
from ._mixin import ParserTestMixin


class TestDHCPFormatParser(ParserTestMixin, TestCase):
    p = DHCPFormatParser()
    basename = 'dhcpd'
    extension = 'conf'

    files = (
        'dhcpd_simple',
        'dhcpd',
    )


