#coding: utf-8
from __future__ import unicode_literals, absolute_import


class ItemList(list):
    name = None
    mode = None

    def __eq__(self, other):
        if isinstance(other, ItemList):
            return bool(set(self) & set(other))
        else:
            return False

    def __ne__(self, other):
        if isinstance(other, ItemList):
            return not bool(set(self) & set(other))
        else:
            return False
