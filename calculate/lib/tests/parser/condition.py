#coding: utf-8
from __future__ import unicode_literals, absolute_import

from calculate.lib.parser.condition.parser import ConditionParser

from unittest import TestCase


class TestConditionParser(TestCase):
    p = ConditionParser()

    def test_simple_expressions(self):
        self.assertTrue(self.p.evaluate('1 < 2'))
        self.assertTrue(self.p.evaluate('1 <= 2'))
        self.assertTrue(self.p.evaluate('2 <= 2'))
        self.assertTrue(self.p.evaluate('2 > 1'))
        self.assertTrue(self.p.evaluate('2 >= 1'))
        self.assertTrue(self.p.evaluate('2 >= 2'))
        self.assertTrue(self.p.evaluate('2 != 1'))
        self.assertTrue(self.p.evaluate('1 == 1'))

        self.assertFalse(self.p.evaluate('1 == 2'))
        self.assertFalse(self.p.evaluate('1 >= 2'))
        self.assertFalse(self.p.evaluate('1 > 2'))
        self.assertFalse(self.p.evaluate('2 <= 1'))
        self.assertFalse(self.p.evaluate('2 < 1'))
        self.assertFalse(self.p.evaluate('2 != 2'))

    def test_composite_conditions(self):
        self.assertTrue(self.p.evaluate('1 == 2 || 2 == 2'))
        self.assertTrue(self.p.evaluate('1 > 2 || 2 >= 2 && 3 == 4 || 3 < 4 '))
        self.assertTrue(self.p.evaluate('1 > 2 || 2 >= 2 && 5 >= 4 || 7 < 4 '))

    def test_nested_conditions(self):
        self.assertTrue(self.p.evaluate('(1 > 2 || 2 >= 2) && (5 >= 4 || 7 < 4) '))
        self.assertTrue(self.p.evaluate('(1 > 2 || 2 >= 2) && (5 >= 4 || 7 < 4) '))

        self.assertFalse(self.p.evaluate('(1 > 2 || 2 >= 2) && (5 == 4 || 7 < 4) '))
        self.assertFalse(self.p.evaluate('(1 > 2 || 2 >= 2) && (5 == 4 || 7 < 4 && 8 == 8) '))

    def test_variable_compute(self):
        self.assertTrue(self.p.evaluate('#-main.cl_env_number-# == 1'))
        self.assertTrue(self.p.evaluate('#-main.cl_env_read_only-# == 100'))
        self.assertTrue(self.p.evaluate('#-main.cl_env_path-# == "/var/calculate"'))

    def test_simple_math(self):
        self.assertTrue(self.p.evaluate('5 == 3 + 2'))
        self.assertTrue(self.p.evaluate('5 < 3 * 2'))
        self.assertTrue(self.p.evaluate('5 > 3 - 2'))
        self.assertTrue(self.p.evaluate('2 == 4 / 2'))

        self.assertFalse(self.p.evaluate('5 == 3* 2'))
        self.assertFalse(self.p.evaluate('5 >= 5 +2'))
        self.assertFalse(self.p.evaluate('5 != 5/1'))

    def test_nested_math(self):
        self.assertTrue(self.p.evaluate('15 == 5 + (5*2)'))
        self.assertTrue(self.p.evaluate('20 == 5 + (5*(2+1))'))

    def test_function_execution(self):
        raise NotImplementedError

    def test_version_compare(self):
        raise NotImplementedError
