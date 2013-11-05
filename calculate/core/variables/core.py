#coding: utf-8
from __future__ import unicode_literals, absolute_import

from calculate.lib.registry.variable import *


class PkgNameVariable(StringVar):
    class Options:
        read_only = True
        system = True

    _value = 'calculate-core'

class PkgVersionVariable(StringVar):
    class Options:
        read_only = True
        system = True

    _value = '1.2.3'
