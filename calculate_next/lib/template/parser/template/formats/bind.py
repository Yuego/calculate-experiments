#coding: utf-8
from __future__ import unicode_literals, absolute_import

from collections import OrderedDict
from pyparsing import *
import six

from calculate_next.lib.template.parser.template.parser import FormatParser


class BindFormatParser(FormatParser):
    comment = ('#', '/*,*/')
    indent = ' '*4
    indent_comments = True

    @classmethod
    def _quoted_string_atom(cls, s, l, t):
        """
        Приводим кавычки к двойным
        """
        return '"{0}"'.format(t[0][1:-1])

    @classmethod
    def _value_atom(cls, s, l, t):
        return {t[0].strip(): t[1].strip()}

    def _simple_atom(self, s, l, t):
        r = OrderedDict()
        comments = {}
        for i, item in enumerate(t):
            if self._is_comment(item):
                comments[i] = item
            else:
                r[item] = None

        r['__comments'] = comments
        return r

    def _statement_atom(self, s, l, t):
        if isinstance(t[1], six.string_types) and not self._is_comment(t[1]):
            key = ' '.join(t[0:2])
            values = t[2:]
        else:
            key = t[0]
            values = t[1:]

        res = OrderedDict()
        res[key] = OrderedDict()
        comments = {}
        for i, val in enumerate(values):
            if isinstance(val, six.string_types):
                comments[i] = val
            else:
                res[key].update(val)
        res[key]['__comments'] = comments
        res['__comments'] = {}
        return res

    def get_syntax(self):
        _semicolon, _lbrace, _rbrace = map(Suppress, ';{}')

        toplevel = Forward()

        comment = self.get_comment_rules()

        value = Word(alphanums + "-_.*!/+^") | quotedString.setParseAction(self._quoted_string_atom)
        key = (value + OneOrMore(value) + _semicolon).setParseAction(self._value_atom)
        simple = (OneOrMore((value + _semicolon) | comment)).setParseAction(self._simple_atom)

        statement = (value
                     + ZeroOrMore(value)
                     + (_lbrace
                        + Optional(toplevel)
                        + _rbrace)
                     + _semicolon).setParseAction(self._statement_atom)

        toplevel << OneOrMore(comment | statement | key | simple)

        return toplevel

    def get_template_syntax(self):
        return None

    def collapse_tree(self, d, depth=0):
        comments = d.pop('__comments')

        result = []
        idx = 0
        tab = self.indent * depth
        comment_tab = tab if self.indent_comments else ''

        for k, v in d.items():
            while idx in comments:
                result.extend(['\n', comment_tab, comments.pop(idx), '\n'])
                idx += 1
            idx += 1

            if v is None:
                result.extend([tab, k, ';\n'])
            elif isinstance(v, six.string_types):
                result.extend([tab, k, ' ', v, ';\n'])
            else:
                result.extend([tab, k, ' {\n',
                               self.collapse_tree(v, depth=depth+1),
                               tab, '};\n'])

        for comment in comments.values():
            result.extend([comment_tab, comment, '\n'])

        return ''.join(result)
