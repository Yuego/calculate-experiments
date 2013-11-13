#coding: utf-8
from __future__ import unicode_literals, absolute_import

from collections import OrderedDict
from pyparsing import *
import six

from calculate_next.lib.template.parser.utils import convert_result
from calculate_next.lib.template.parser.template.parser import FormatParser


class INIFormatParser(FormatParser):
    comment = ('#', ';')

    def _value_atom(self, s, l, t):
        return OrderedDict({t[0].strip(): t[1].strip()})

    def _section_atom(self, s, l, t):
        v = convert_result(t[-1])
        comments = {}
        values = OrderedDict()
        for i, val in enumerate(v):
            if isinstance(val, six.string_types):
                comments[i] = val
            else:
                values.update(val)
        values['__comments'] = comments
        t[-1] = values
        return six.moves.reduce(lambda x, y: {y: x}, t[::-1])

    def get_syntax(self):
        _command = Word('!^+-', exact=1)
        _lbrack = Literal('[')
        _rbrack = Literal(']')
        _equals = Suppress('=')

        _comment = self.get_comment_rules()

        _section_name = Word(printables, excludeChars=']')
        _key = (~_lbrack + Word(printables, excludeChars='=') + _equals + restOfLine).setParseAction(self._value_atom)

        _section = Combine(Optional(_command) + _lbrack + _section_name + _rbrack)

        section = (_section
                   + Group(ZeroOrMore(_key | _comment))
                   ).setParseAction(self._section_atom)

        syntax = ZeroOrMore(section | _comment)

        return syntax

    def get_template_syntax(self):
        return None

    def collapse_tree(self, d, indent=None, indent_comments=False, depth=0):
        comments = d.pop('__comments')
        result = []
        idx = 0
        tab = ' '*depth*indent if indent is not None else ''
        comment_tab = tab if indent_comments else ''

        for k, v in d.items():
            while(idx in comments):
                result.extend([comment_tab, comments.pop(idx), '\n'])
                idx += 1
            idx += 1

            if isinstance(v, six.string_types):
                result.extend([tab, k, '=', v, '\n'])
            else:
                result.extend([
                    tab, '\n', k, '\n', self.collapse_tree(v,
                                                             indent=indent,
                                                             indent_comments=indent_comments,
                                                             depth=depth+1)
                ])

        for comment in comments.values():
            result.extend([comment_tab, comment, '\n'])

        return ''.join(result)
