#coding: utf-8
from __future__ import unicode_literals, absolute_import

from calculate_next.lib.registry.variable import *


class ClCorePkgNameVariable(StringVar):
    class Options:
        read_only = True
        system = True

    _value = 'calculate-core'

class ClCorePkgVersionVariable(StringVar):
    class Options:
        read_only = True
        system = True

    _value = '1.2.3'
