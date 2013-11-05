#coding: utf-8
from __future__ import unicode_literals, absolute_import





class Function(object):

    def __init__(self, expression):
        self.expression = expression

    def apply(self):
        raise NotImplementedError

    @property
    def result(self):
        if not hasattr(self, '_result'):
            setattr(self, '_result', self.apply())
        return self._result

    def __str__(self):
        return str(self.__unicode__())

    def __unicode__(self):
        return '{0}({1})'.format(self.__class__.__name__[:-8].lower(), self.expression)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.result == other

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        return self.result > other

    def __ge__(self, other):
        return self.result >= other

    def __lt__(self, other):
        return self.result < other

    def __le__(self, other):
        return self.result <= other


class MergeFunction(Function):

    def apply(self):
        """
        Проверить, что выражение является именем пакета
        Вернуть версию этого пакета
        """
        pass

class LoadFunction(Function):
    pass

class PKGFunction(Function):
    pass

functions = {
    'merge': MergeFunction,
    'load': LoadFunction,
    'pkg': PKGFunction,
}
