#coding: utf-8
from __future__ import unicode_literals, absolute_import

from pyparsing import *

from calculate_next.lib.template.parser.template.parser import FormatParser

#TODO: поддержка многострочных параметров
class SquidFormatParser(FormatParser):
    comment = '#'

    @classmethod
    def _value_atom(cls, s, l, t):
        if t[0] in ('acl', 'header_access', 'header_replace'):
            key = ' '.join(t[:2])
            value = ' '.join(t[2:]).strip()
        elif t[0] in ('http_access',):
            key = ' '.join(t)
            value = None
        else:
            key = t[0]
            value = ' '.join(t[1:]).strip()
        return {key.strip(): value}

    def get_syntax(self):
        _command = '!^+-'
        _value_name_start = _command + alphanums

        comment = self.get_comment_rules()

        value = (Word(_value_name_start, printables)
                 + OneOrMore(~Suppress(LineEnd()) + Word(printables))
                 ).setParseAction(self._value_atom)

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

            if v is None:
                result.extend([k, '\n'])
            else:
                result.extend([k, ' ', v, '\n'])

        for comment in comments.values():
            result.extend([comment, '\n'])

        return ''.join(result)
