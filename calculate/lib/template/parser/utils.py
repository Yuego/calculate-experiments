#coding: utf-8
from __future__ import unicode_literals, absolute_import

from pyparsing import ParseResults


def convert_result(res):
    __convert = lambda x: x.asList()[0] if isinstance(x, ParseResults) else x
    return list(map(__convert, res))
