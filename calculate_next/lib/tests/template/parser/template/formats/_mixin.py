#coding: utf-8
from __future__ import unicode_literals, absolute_import

import codecs
from collections import OrderedDict
from copy import deepcopy
import os


class ParserTestMixin(object):
    files = ()
    merge_files = ('merge',)
    basepath = 'data/tests/configs'
    basename = ''
    extension = ''

    def _open_file(self, f):
        with codecs.open(f, mode='r', encoding='utf-8') as txt:
            return txt.read()

    def _compare_dicts(self, d1, d2):
        for a, b in zip(d1.items(), d2.items()):
            for x, y in zip(a, b):
                if isinstance(x, (dict, OrderedDict)):
                    self._compare_dicts(x, y)
                else:
                    self.assertEqual(x, y)

    def test_parse(self):
        extension = '.{0}'.format(self.extension) if self.extension else ''

        for f in self.files:
            filepath = os.path.join(self.basepath, self.basename,
                                    f + extension)
            first_content = self._open_file(filepath)
            first_tree = self.p.parse(first_content)

            self.assertIsInstance(first_tree, OrderedDict)

            second_content = self.p.collapse_tree(deepcopy(first_tree))
            second_tree = self.p.parse(second_content)

            self._compare_dicts(first_tree, second_tree)

    def test_merge(self):
        extension = '.{0}'.format(self.extension) if self.extension else ''

        for f in self.merge_files:
            src, dst, result = map(
                lambda x: os.path.join(
                    self.basepath, self.basename, f,
                    x + extension),
                    ['src', 'dst', 'result'])

            dst_tree = self.p.parse(self._open_file(dst))
            src_tree = self.p.parse(self._open_file(src))

            #print '!!!!!!!!!!!!!!!'
            #print src_tree
            #print '---------------'
            #print dst_tree

            merged_tree = self.p.merge(dst_tree, src_tree)
            sample_tree = self.p.parse(self._open_file(result))

            #print '==============='
            #print merged_tree
            #print '---------------'
            #print sample_tree
            #print '==============='

            self._compare_dicts(sample_tree, merged_tree)
