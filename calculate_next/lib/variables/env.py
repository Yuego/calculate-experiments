#coding: utf-8
from __future__ import unicode_literals, absolute_import

from calculate_next.lib.registry.variable import *


class ClEnvPathVariable(StringVar):
    value = '/var/calculate'


class ClEnvNumberVariable(IntegerVar):
    value = 1


class ClEnvReadOnlyVariable(ReadOnlyIntegerVar):
    value = 100


class ClEnvFlagVariable(BooleanVar):
    value = False


_env_data = [('system', '/etc/calculate/calculate.env'),
            ('local', '/var/calculate/calculate.env'),
            ('remote', '/var/calculate/remote/calculate.env')]

