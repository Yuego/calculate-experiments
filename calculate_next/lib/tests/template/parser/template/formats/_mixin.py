#coding: utf-8
from __future__ import unicode_literals, absolute_import

import codecs
from collections import OrderedDict
from copy import deepcopy

class ParserTestMixin(object):
    files = ()
    merge_files = ()

    def _open_file(self, f):
        return codecs.open(f, mode='r', encoding='utf-8').read()

    def _compare_dicts(self, d1, d2):
        for a, b in zip(d1.items(), d2.items()):
            for x, y in zip(a, b):
                #print x, y
                if isinstance(x, OrderedDict):
                    self._compare_dicts(x, y)
                else:
                    self.assertEqual(x, y)

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

            self._compare_dicts(first_tree, second_tree)

    def test_merge(self):
        self.assertEqual(len(self.merge_files), 3)

        dst = self._open_file(self.merge_files[0])
        src = self._open_file(self.merge_files[1])

        syntax = self.p.get_original_syntax()

        dst_tree = self.p.expand_tree(syntax.parseString(dst, parseAll=True))
        src_tree = self.p.expand_tree(syntax.parseString(src, parseAll=True))

        merged_tree = self.p.merge(dst_tree, src_tree)

        sample = self._open_file(self.merge_files[2])
        sample_tree = self.p.expand_tree(syntax.parseString(sample, parseAll=True))

        #print '==============='
        #print merged_tree
        #print '---------------'
        #print sample_tree
        #print '==============='

        self._compare_dicts(sample_tree, merged_tree)


