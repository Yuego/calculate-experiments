#coding: utf-8
from __future__ import unicode_literals, absolute_import

from unittest import TestCase

from calculate_next.lib.version import Version as V


class TestVersion(TestCase):

    def test_compare(self):
        self.assertTrue(V('1') < V('2'))
        self.assertTrue(V('1.3') == V('1.3'))
        self.assertTrue(V('1.5.1') > V('1.5'))
        self.assertTrue(V('1.2_rc5' < '1.2'))
        self.assertTrue(V('1.3') != '1.3-r1')
        self.assertTrue(V('1.5.1') >= V('1.5'))
        self.assertTrue(V('1.5.1') >= V('1.5.1'))
        self.assertTrue(V('1.5_beta1') <= '1.5')
        self.assertTrue(V('1.5_beta1') <= '1.5_beta1')
