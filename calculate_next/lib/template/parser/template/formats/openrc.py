#coding: utf-8
from __future__ import unicode_literals, absolute_import

from collections import OrderedDict
from pyparsing import *

from calculate_next.lib.template.parser.template.parser import FormatParser


class OpenRCFormatParser(FormatParser):
    comment = '#'

    @classmethod
    def _value_atom(cls, s, l, t):
        return OrderedDict({t[0].strip(): t[1].strip()})

    def get_syntax(self):
        _command = '!^+-'
        _value_name = alphanums + '_'
        _value_name_start = _command + _value_name

        _equals = Suppress('=')

        comment = self.get_comment_rules()

        value = (Word(_value_name_start, _value_name) + _equals + restOfLine).setParseAction(self._value_atom)

        syntax = ZeroOrMore(comment | value)

        return syntax

    def collapse_tree(self, d, depth=0):
        comments = d.pop('__comments')
        result = []
        idx = 0
        for k, v in d.items():
            while idx in comments:
                result.extend([comments.pop(idx), '\n'])
                idx += 1
            idx += 1

            result.extend([k, '=', v, '\n'])

        for comment in comments.values():
            result.extend([comment, '\n'])

        return ''.join(result)
