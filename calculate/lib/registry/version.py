#coding: utf-8
from __future__ import unicode_literals, absolute_import

from portage.versions import vercmp


class Version(unicode):
    def __init__(self, string, encoding=None, errors='strict'):
        super(Version, self).__init__(string, encoding, errors)

    def __gt__(self, other):
        return vercmp(self, other) > 0

    def __ge__(self, other):
        return self.__eq__(other) or self.__gt__(other)

    def __lt__(self, other):
        return vercmp(self, other) < 0

    def __le__(self, other):
        return self.__eq__(other) or self.__lt__(other)
