#coding: utf-8
from __future__ import unicode_literals, absolute_import

from pyparsing import ParseException
import six
from unittest import TestCase

from calculate.lib.template.parser.header.parser import TemplateHeaderParser, DirectoryHeaderParser

c = '# Calculate '


class ParamsMixin(object):

    def _quote_string(self, s):
        if ' ' in s:
            return '"{0}"'.format(s)
        return s

    def _join_params(self, params_dict, condition=None):
        params = c + ' '.join((
                              '='.join([x, self._quote_string(y)]) if isinstance(y, six.string_types) else x)
                              for x, y in params_dict.items())
        if condition is not None:
            params = ' '.join([params, condition])

        return params

    def _test_params(self, params_dict, condition=None):
        params = self._join_params(params_dict, condition)
        self.assertDictEqual(self.p.evaluate(params), params_dict)

    def _test_wrong_params(self, params_dict, condition=None):
        params = self._join_params(params_dict, condition)
        self.assertRaises(ParseException, self.p.evaluate, *(params,))

    def test_conditions(self):
        self.assertDictEqual(self.p.evaluate(c + '1 < 2'), {})
        self.assertDictEqual(self.p.evaluate(c + '1 < 2 5+8 > 12 '), {})

        # False condition
        self.assertIsNone(self.p.evaluate(c + '1 < 2 5+8 > 12 6 <= 2'))


class TestTemplateHeaderParser(ParamsMixin, TestCase):
    p = TemplateHeaderParser()

    def test_params(self):

        self._test_params({
            'append': 'patch',
            'format': 'patch',
            'force': True,
        })

        self._test_params({
            'merge': 'app-misc/mc',
            'force': True,
            'multiline': True,
        }, '4 < 5 && main.cl_env_read_only > 10')

        self._test_wrong_params({
            'append': 'unknown',
        })


class TestDirectoryHeaderParser(ParamsMixin, TestCase):
    p = DirectoryHeaderParser()

    def test_params(self):

        self._test_params({
            'append': 'clear',
            'path': '/var/calculate',
            'name': 'some name',
            'force': True,
        })

        self._test_wrong_params({
            'append': 'after',
        })
