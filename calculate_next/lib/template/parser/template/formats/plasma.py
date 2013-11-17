#coding: utf-8
from __future__ import unicode_literals, absolute_import

from pyparsing import *

from .ini import INIFormatParser


class PlasmaFormatParser(INIFormatParser):
    sort_keys = True

    def get_syntax(self):
        _command = Word('!^+-', exact=1)
        _lbrack, _rbrack = map(Literal, '[]')
        _equals = Suppress('=')

        _comment = self.get_comment_rules()

        _section_name = Word(printables, excludeChars=']')
        _key = (~_lbrack + Word(printables, excludeChars='=') + _equals + restOfLine).setParseAction(self._value_atom)

        _section = (_lbrack + _section_name + _rbrack)

        section = (Combine(Optional(_command) + _section + ZeroOrMore(_section) + White().suppress())
                  + Group(ZeroOrMore(_comment | _key))
                  ).setParseAction(self._section_atom)

        syntax = ZeroOrMore(_comment | section)

        return syntax
