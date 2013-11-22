#coding: utf-8
from __future__ import unicode_literals, absolute_import

from collections import OrderedDict
from pyparsing import *
import six

from calculate_next.lib.template.parser.template.collections import ItemList
from .bind import BindFormatParser


class DHCPFormatParser(BindFormatParser):
    comment = '#'

    @classmethod
    def _block_atom(cls, s, l, t):
        if t[0].endswith('pool'):
            items = ItemList()
            items.name = 'pool'
            if t[0][0] in cls.STRATS:
                items.mode = t[0][0]

            for item in t[1]:
                if isinstance(item, six.string_types):
                    items.append(item)
                else:
                    items.append(' '.join(item.popitem()))

            return {'pool': items}
        if t[0].endswith('subnet'):
            key = ' '.join(t[0:4])
            values = t[4]
        else:
            key = ' '.join(t[0:2])
            values = t[2]

        comments = {}
        data = OrderedDict({key: OrderedDict()})
        for idx, val in enumerate(values):
            if isinstance(val, six.string_types):
                comments[idx] = val
            elif 'pool' in val:
                data[key].setdefault('pool', []).append(val['pool'])
            else:
                data[key].update(val)
        data[key]['__comments'] = comments

        return data

    @classmethod
    def _value_atom(cls, s, l, t):
        if t[0] in ('set', 'option', 'hardware'):
            return {' '.join(t[0:2]).strip(): ' '.join(t[2:]).strip()}
        else:
            return {t[0].strip(): ' '.join(t[1:]).strip()}

    def get_syntax(self):
        _semicolon, _lbrace, _rbrace = map(Suppress, ';{}')
        _command = '!+-^'
        _name_start = alphanums + _command

        comment = self.get_comment_rules()

        root = Forward()

        value = (
            OneOrMore(
                Word(_name_start, alphanums + '-_.:')
                | Literal('=')
                | QuotedString(quoteChar='(', endQuoteChar=')', unquoteResults=False)
                | QuotedString(quoteChar='"', unquoteResults=False)
            ) + _semicolon
        ).setParseAction(self._value_atom)

        block = (OneOrMore(Word(_name_start, alphanums + '-.')
                           | QuotedString(quoteChar='"', unquoteResults=False)
                           )
                 + _lbrace
                 + Group(root)
                 + _rbrace
                 ).setParseAction(self._block_atom)

        root << ZeroOrMore(comment | value | block)
        return root

    def collapse_tree(self, d, depth=0):
        result = []
        tab = self.indent * depth
        comments = d.pop('__comments')
        idx = 0
        comment_tab = tab if self.indent_comments else ''

        for k, v in d.items():
            while idx in comments:
                result.extend(['\n', comment_tab, comments.pop(idx), '\n'])
                idx += 1
            idx += 1

            if v == '':
                result.extend([tab, k, ';\n'])
            elif isinstance(v, six.string_types):
                result.extend([tab, k, ' ', v, ';\n'])
            elif isinstance(v, list):
                for item in v:
                    result.extend([tab, k, ' {\n'])
                    for s in item:
                        if self._is_comment(s):
                            result.extend([comment_tab, self.indent, s, '\n'])
                        else:
                            result.extend([tab, self.indent, s, ';\n'])
                    result.extend([tab, '}\n'])
            else:
                result.extend([tab, k, ' {\n',
                               self.collapse_tree(v, depth=depth+1),
                               tab, '}\n'])

        for comment in comments.values():
            result.extend([comment_tab, comment, '\n'])

        return ''.join(result)
