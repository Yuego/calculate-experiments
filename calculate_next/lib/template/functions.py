#coding: utf-8
from __future__ import unicode_literals, absolute_import

from functools import wraps

class Function(object):
    args = 0

    def __init__(self, *args):
        assert len(args) == self.args, '{0}() takes exactly {1} arguments ({2} given)'.format(
            self.__class__.__name__[:-8].lower(), self.args, len(args)
        )
        self._args = args

    def apply(self):
        raise NotImplementedError

    @property
    def result(self):
        if not hasattr(self, '_result'):
            setattr(self, '_result', self.apply())
        return self._result

    def __str__(self):
        return self.__repr__()

    def __unicode__(self):
        return self.__repr__()

    def __repr__(self):
        return '{0}({1})'.format(self.__class__.__name__[:-8].lower(), ','.join(map(repr, self._args)))

    def __nonzero__(self):
        return bool(self.apply())

    def __bool__(self):
        return self.__nonzero__()

    def __eq__(self, other):
        return self.apply() == other

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        return self.apply() > other

    def __ge__(self, other):
        return self.apply() >= other

    def __lt__(self, other):
        return self.apply() < other

    def __le__(self, other):
        return self.apply() <= other

    def __add__(self, other):
        return self.apply() + other

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        return self.apply() - other

    def __rsub__(self, other):
        return other - self.apply()

    def __mul__(self, other):
        return self.apply() * other

    def __rmul__(self, other):
        return self.__mul__(other)

    def __div__(self, other):
        return self.apply() / other

    def __rdiv__(self, other):
        return other / self.apply()


class MergeFunction(Function):
    args = 1

    def apply(self):
        """
        Проверить, что выражение является именем пакета
        Вернуть версию этого пакета
        """
        return '1.2.3'


class LoadFunction(Function):
    pass


class PKGFunction(Function):
    pass

class TestFunction(Function):
    args = 3

    def apply(self):
        return 5

functions = {
    'merge': MergeFunction,
    'load': LoadFunction,
    'pkg': PKGFunction,
    'test': TestFunction,
}
