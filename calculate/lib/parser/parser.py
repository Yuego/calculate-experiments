#coding: utf-8
from __future__ import unicode_literals, absolute_import

class ParseFinishedException(Exception):
    pass

class SyntaxParser(object):

    """
    Упорядоченный список типов объектов

    - упорядочен по убыванию приоритета
    """
    _types = ()

    _states = ('begin',)

    _state_machine = {0: [0]}

    def __init__(self):
        self._prev_state = None
        self._state = 0

        self._result = None

    def _s(self, name):
        """Возвращает метод состояния с именем name"""
        return getattr(self, '_state_' + name)

    def _get_item_type(self):
        raise NotImplementedError

    def parse(self, syntax):
        raise NotImplementedError
