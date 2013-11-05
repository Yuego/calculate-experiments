#coding: utf-8
from __future__ import unicode_literals, absolute_import

from unittest import TestCase

from calculate.lib.template.header import TemplateHeaderParser
from calculate.lib.template.functions import functions as f
from calculate.lib.template.params import parameters as p

class HeaderParserTest(TestCase):

    def setUp(self):
        self.th = TemplateHeaderParser()

    def test_empty(self):
        self.th.parse('')

        self.assertListEqual(self.th.expressions, [])
        self.assertDictEqual(self.th.options, {})

    def test_simple_variable(self):
        self.th.parse('  path=value  ')

        self.assertListEqual(self.th.expressions, [])
        self.assertDictEqual(self.th.options, {'path': 'value'})

    def test_quoted_variable(self):
        self.th.parse('  name="some value"  ')

        self.assertListEqual(self.th.expressions, [])
        self.assertDictEqual(self.th.options, {'name': 'some value'})

    def test_empty_param_value(self):
        self.th.parse('name= surname=zzz')

        self.assertListEqual(self.th.expressions, [])
        self.assertDictEqual(self.th.options, {'name': '', 'surname': 'zzz'})

    def test_simple_expression_variable(self):
        self.th.parse('cl_desktop_xsession==gnome')

        self.assertListEqual(self.th.expressions, [['cl_desktop_xsession', '==', 'gnome']])
        self.assertDictEqual(self.th.options, {})

    def test_simple_expression_function(self):
        self.th.parse('merge(app-misc/mc)>=1.2.3')

        #print self.th.value
        #print self.th.options
        #print self.th.expressions

        self.assertListEqual(self.th.expressions, [[f['merge']('app-misc/mc'), '>=', '1.2.3']])
        self.assertDictEqual(self.th.options, {})

    def test_simple_expression(self):
        self.th.parse('name= path="#-ini(resource.desktop)-#" cl_desktop_xsession==gnome')

        self.assertListEqual(self.th.expressions, [['cl_desktop_xsession', '==', 'gnome']])
        self.assertDictEqual(self.th.options, {'path': '#-ini(resource.desktop)-#', 'name': ''})

    def test_expression_and_operation(self):
        self.th.parse('cl_desktop_xsession==gnome&&merge(app-misc/mc)!=1.2.3')

        self.assertListEqual(self.th.expressions, [['cl_desktop_xsession', '==', 'gnome'], '&&', [f['merge']('app-misc/mc'), '!=', '1.2.3']])
        self.assertDictEqual(self.th.options, {})

    def test_very_long_expression(self):
        pass
        #self.th.parse('name=Default link=/etc/gdm/PostSession/Default.old mirror load(/etc/gdm/PostSession/Default.old)!=   merge()!=&&pkg()>=3.0 append=skip')

        #print self.th.value
        #print self.th.options
        #print self.th.expressions


from calculate.lib.template.parser import *


class FunctionParameterParserTest(TestCase):

    def setUp(self):
        self.p = FunctionParametersParser()

    def test_one_param(self):
        _z = ['key']

        r = self.p.parse('key')
        r1 = self.p.parse(' key')
        r2 = self.p.parse(' key \t')

        self.assertListEqual(_z, r)
        self.assertListEqual(_z, r1)
        self.assertListEqual(_z, r2)

    def test_two_params(self):
        _z = ['key', 'val']

        r = self.p.parse('key,val')
        r1 = self.p.parse('\t  key\t , val ')

        self.assertListEqual(_z, r)
        self.assertListEqual(_z, r1)

    def test_multiple_params(self):
        _z = ['key1', 'key2', 'key3', 'key4']

        r = self.p.parse(' key1, key2\t,\t key3,key4')

        self.assertListEqual(_z, r)

    def test_exceptions(self):
        _wrong_begin = ',key'
        _wrong_begin2 = 'key,,val'
        _wrong_end = 'key val'

        self.assertRaises(UnexpectedSymbolException, self.p.parse, [_wrong_begin])
        self.assertRaises(UnexpectedSymbolException, self.p.parse, [_wrong_begin2])
        self.assertRaises(UnexpectedSymbolException, self.p.parse, [_wrong_end])

class ExpressionParserTest(TestCase):

    def setUp(self):
        self.p = ExpressionParser()
