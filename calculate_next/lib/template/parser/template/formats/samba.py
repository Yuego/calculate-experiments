#coding: utf-8
from __future__ import unicode_literals, absolute_import

from pyparsing import *
import six

from .ini import INIFormatParser



class SambaFormatParser(INIFormatParser):

    def get_original_syntax(self):
        _lbrack = Suppress('[')
        _rbrack = Suppress(']')
        _equals = Suppress('=')

        _comment = self.get_comment_rules()

        _section_name = Word(printables, excludeChars=']')
        _key = (Word(printables + ' \t', excludeChars='=' + ''.join(self._get_comment_starts())) + _equals + restOfLine).setParseAction(self._value_atom)

        _section = (_lbrack + _section_name + _rbrack)

        section = (_section
                   + Group(ZeroOrMore(_key | _comment))
                   ).setParseAction(self._section_atom)

        syntax = ZeroOrMore(section | _comment)

        return syntax

    def collapse_tree(self, d, indent=None, indent_comments=False, depth=0):
        return super(SambaFormatParser, self).collapse_tree(d,
                                                            indent=4,
                                                            indent_comments=indent_comments,
                                                            depth=depth)
