#coding: utf-8
from __future__ import unicode_literals, absolute_import

from calculate.lib.registry.variable import *


class PathVariable(StringVar):
    _value = '/var/calculate'

class NumberVariable(IntegerVar):
    _value = 1

class ReadOnlyVariable(IntegerVar):
    _value = 100

    class Options:
        read_only = True


class FlagVariable(BooleanVar):
    _value = False
