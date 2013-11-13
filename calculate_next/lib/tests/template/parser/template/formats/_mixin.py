#coding: utf-8
from __future__ import unicode_literals, absolute_import

import codecs
from collections import OrderedDict
from copy import deepcopy

class ParserTestMixin(object):
    files = ()

    def _open_file(self, f):
        return codecs.open(f, mode='r', encoding='utf-8').read()

    def _compare_dict(self, d1, d2):
        result = True
        for a, b in zip(d1.items(), d2.items()):
            for x, y in zip(a, b):
                #print x, y
                if isinstance(x, OrderedDict):
                    result = self._compare_dict(x, y)
                else:
                    result = x == y

                if not result:
                    return result

            if not result:
                return result

        return result

    def test_original_parser(self):
        syntax = self.p.get_original_syntax()

        for f in self.files:
            first_content = self._open_file(f)
            first_result = syntax.parseString(first_content, parseAll=True)
            first_tree = self.p.expand_tree(first_result)

            self.assertIsInstance(first_tree, OrderedDict)

            second_content = self.p.collapse_tree(deepcopy(first_tree))
            second_result = syntax.parseString(second_content, parseAll=True)
            second_tree = self.p.expand_tree(second_result)

            self.assertEqual(self._compare_dict(first_tree, second_tree), True)
