#coding: utf-8
from __future__ import unicode_literals, absolute_import

import unittest

from calculate_next.lib.template.parser.header.parser import TemplateHeaderParser


class TestHeaders(unittest.TestCase):
    p = TemplateHeaderParser()

    def test_headers(self):
        failures = 0
        with open('./headers.txt', 'r') as h:
            with open('./failed_headers.txt', 'w') as f:
                f.truncate()
                f.seek(0)
                for l in h.readlines():
                    try:
                        self.p.evaluate(l)
                    except Exception as e:
                        failures = failures + 1
                        f.write('Failed: {0}\twith args: {1}\n\n'.format(l, ', '.join(e.args)))

        self.assertEqual(failures, 0)

if __name__ == '__main__':
    unittest.main()
