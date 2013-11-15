#coding: utf-8
from __future__ import unicode_literals, absolute_import

from collections import OrderedDict


def compare_dicts(d1, d2):
    try:
        for a, b in zip(d1.items(), d2.items()):
            for x, y in zip(a, b):
                if isinstance(x, (dict, OrderedDict)):
                    compare_dicts(x, y)
                else:
                    assert x == y, 'Items `{0}` and `{1}` isn`t equal!'
    except AssertionError:
        return False
    else:
        return True
