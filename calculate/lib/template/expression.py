#coding: utf-8
from __future__ import unicode_literals, absolute_import

import string

_name_begin_chars = string.ascii_lowercase + '_'
_name_chars = _name_begin_chars + string.digits

class UnexpectedSymbolException(Exception):
    pass

class InvalidTokenException(Exception):
    pass

'''
    0 - начало работы. Ожидаем пробельные символы или буквы или символ подчеркивания

'''

class Parser(object):

    def __init__(self, value):
        self._state = []
        self._val = value
        self._pos = 0
        self._idx = 0
        self.state = 'begin'
        self._stack = []

    def push_state(self, name):
        self._state.append([
            self._pos, self._idx, self._stack[:]
        ])

    def pop_state(self):
        self._pos, self._idx, self._stack = self._state.pop()

    def push(self, value):
        self._stack.append(value)

    def pop(self, c=1):
        assert isinstance(c, int) and c > 0, 'Invalid count!'

        ret = self._stack[:c:-1]
        self._stack = self._stack[:-c]

        return ret

    @property
    def ch(self):
        return self._val[self._idx]

    def _s(self, name):
        _sname = '_state_' + name
        if hasattr(self, _sname):
            return getattr(self, _sname)
        else:
            raise AttributeError(_sname)

    def _state_begin(self):
        c = self.ch
        if c in ' \t':
            self._pos = self._idx = self._idx + 1
        elif c.lower() in _name_begin_chars:
            self.state = 'wait_for_token'
        else:
            raise UnexpectedSymbolException()

    def _state_end(self):
        pass

    def _state_wait_for_token(self):
        c = self.ch
        if c.lower() not in _name_chars:
            self.push(self._val[self._pos:self._idx])
            self._pos = self._idx

        self._idx += 1

    def parse(self):
        _len = len(self._val)
        while(self._idx < _len):
            self._s(self.state)()

        self._state_end()

