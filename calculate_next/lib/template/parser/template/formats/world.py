#coding: utf-8
from __future__ import unicode_literals, absolute_import

from pyparsing import *

from calculate_next.lib.template.parser.rules import slotted_package_atom
from calculate_next.lib.template.parser.template.parser import FormatParser


class WorldFormatParser(FormatParser):
    comment = '#'

    @classmethod
    def _value_atom(cls, s, l, t):
        return {t[0].strip(): None}

    def get_syntax(self):
        _command = Word('!^+-', exact=1)

        comment = self.get_comment_rules()

        value = Combine(Optional(_command) + slotted_package_atom).setParseAction(self._value_atom)

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

            result.extend([k, '\n'])

        for comment in comments.values():
            result.extend([comment, '\n'])

        return ''.join(result)
