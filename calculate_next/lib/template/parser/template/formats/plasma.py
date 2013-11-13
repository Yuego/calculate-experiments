#coding: utf-8
from __future__ import unicode_literals, absolute_import

from collections import OrderedDict
from pyparsing import *
import six

from calculate_next.lib.template.parser.utils import convert_result
from .ini import INIFormatParser



class PlasmaFormatParser(INIFormatParser):

    def _section_atom(self, s, l, t):
        t[0] = ']['.join(t[0])
        return super(PlasmaFormatParser, self)._section_atom(s, l, t)

    def get_original_syntax(self):
        _lbrack = Suppress('[')
        _rbrack = Suppress(']')
        _equals = Suppress('=')

        _comment = self.get_comment_rules()

        _section_name = Word(printables, excludeChars=']')
        _key = (~_lbrack + Word(printables, excludeChars='=') + _equals + restOfLine).setParseAction(self._value_atom)

        _section = (_lbrack + _section_name + _rbrack)

        section = (Group(_section + ZeroOrMore(_section))
                   + Group(ZeroOrMore(_key | _comment))
                   ).setParseAction(self._section_atom)

        syntax = ZeroOrMore(section | _comment)

        return syntax
