#coding: utf-8
from __future__ import unicode_literals, absolute_import

from pyparsing import *
import six

from .bind import BindFormatParser


#TODO: корректно обрабатывать !include в конфиге
class DovecotFormatParser(BindFormatParser):
    comment = '#'

    def get_syntax(self):
        _lbrace, _rbrace, _equal = map(Suppress, '{}=')
        _command = '!+-^'
        _name_start = _command + alphas

        comment = self.get_comment_rules()

        root = Forward()

        value = (Word(_name_start, alphanums + '_')
                 + _equal
                 + restOfLine
                 ).setParseAction(self._value_atom)

        block = (Word(_name_start, alphanums)
                 + Optional(Word(alphanums))
                 + _lbrace
                 + root
                 + _rbrace
                 ).setParseAction(self._statement_atom)

        root << ZeroOrMore(comment | value | block)

        return root

    def collapse_tree(self, d, depth=0):
        comments = d.pop('__comments')

        result = []
        idx = 0
        tab = self.indent * depth
        comment_tab = tab if self.indent_comments else ''

        for k, v in d.items():
            while idx in comments:
                result.extend([comment_tab, comments.pop(idx), '\n'])
                idx += 1
            idx += 1

            if v is None:
                result.extend([tab, k, ' =\n'])
            elif isinstance(v, six.string_types):
                result.extend([tab, k, ' = ', v, '\n'])
            else:
                result.extend([tab, k, ' {\n',
                               self.collapse_tree(v, depth=depth+1),
                               tab, '}\n\n'])

        for comment in comments.values():
            result.extend([comment_tab, comment, '\n'])

        return ''.join(result)
