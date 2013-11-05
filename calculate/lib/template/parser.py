#coding: utf-8
from __future__ import unicode_literals, absolute_import

import string

_name_chars = string.ascii_lowercase + '_' + string.digits

class UnexpectedSymbolException(Exception):
    pass

class InvalidTokenException(Exception):
    pass


class Parser(object):

    def __init__(self):
        self._val = ''
        self._pos = 0
        self._stack = []
        self._states_stack = []
        self._result = []

        self.states = {
            'begin': self._state_begin,
            'end': self._state_end,

            'wait_for_token_char': self._state_wait_for_token_char,
        }

    def push(self, value):
        self._stack.append(value)

    def pop(self, c=1):
        assert isinstance(c, int) and c > 0, 'Invalid count!'

        ret = self._stack[:c:-1]
        self._stack = self._stack[:-c]

        return ret

    def pop_all(self):
        ret = self._stack[:]
        self._stack = []
        return ret

    def push_state(self, state):
        self._states_stack.append(state)

    def pop_state(self):
        self._states_stack.pop()

    def _state_begin(self, idx):
        c = self._val[idx]
        if c in ' \t':
            self._pos = idx + 1
        elif c.lower() in _name_chars:
            self.state = 'wait_for_token_char'
        else:
            raise UnexpectedSymbolException()

    def _state_end(self, idx):
        pass

    def _state_wait_for_token_char(self, idx):
        pass

    def parse(self, value):
        self._val = value
        self.state = 'begin'

        for i in range(len(self._val)):
            self.states.get(self.state)(i)

        self._state_end(len(self._val))

        return self.get_result()

    def get_result(self):
        return self._result


class FunctionParametersParser(Parser):
    
    def __init__(self):
        super(FunctionParametersParser, self).__init__()
        self.states.update({
            'wait_for_comma': self._state_wait_for_comma,
        })

    def _state_wait_for_token_char(self, idx):
        c = self._val[idx]
        if c.lower() in _name_chars:
            pass
        else:
            self.state = 'wait_for_comma'
            self._state_wait_for_comma(idx)

    def _state_wait_for_comma(self, idx):
        c = self._val[idx]
        if c in ' \t':
            pass
        elif c == ',':
            self.push(self._val[self._pos:idx].strip())
            self._pos = idx + 1
            self.state = 'begin'
        else:
            raise UnexpectedSymbolException('{}:{} - {}'.format(self._pos, idx, c))

    def _state_end(self, idx):
        if self._pos != idx:
            self.push(self._val[self._pos:idx].strip())

    def get_result(self):
        self._result = self.pop_all()
        return super(FunctionParametersParser, self).get_result()


class ExpressionParser(Parser):

    def __init__(self):
        super(ExpressionParser, self).__init__()

    def _state_wait_for_token_char(self, idx):
        c = self._val[idx]
        if c in _name_chars:
            pass

class ConditionParser(Parser):
    pass


class _ExpressionParser(Parser):

    def __init__(self):
        super(ExpressionParser, self).__init__()
        self.states.update({
            'expression': self._state_expression,

            'wait_for_right_bracket': self._state_wait_for_right_bracket,
            'wait_for_symbol': self._state_wait_for_symbol,
        })

    def _wait_for_token_char(self, idx):
        c = self._val[idx]
        if c in _name_chars:
            pass
        elif c == '(':  # Похоже, что это функция
            self.push(self._val[self._pos:idx])
            self._pos = idx + 1
            self.state = 'wait_for_right_bracket'
        else:
            self.state = 'wait_for_symbol'
            self._state_wait_for_symbol(idx)

    def _state_wait_for_symbol(self, idx):
        if self._pos == idx:
            c = self._val[idx]
            if c in '<>' and self._val[idx + 1] not in '!=<>':
                self.state = 'expession_value'
                self._stack.append(c)
                self._pos = idx + 1
        elif self._pos == idx - 1:
            c = self._val[self._pos:idx + 1]
            if c in ['!=', '==', '>=', '<=']:
                self.state = 'end'
                self._stack.append(c)
                self._pos = idx + 1
            else:
                raise InvalidTokenException('Некорректный токен `{0}`'.format(c))

    def _state_wait_for_right_bracket(self, idx):
        c = self._val[idx]
        if c == ')':
            fp_parser = FunctionParametersParser()
            _params_string = self._val[self._pos:idx]
            _params = fp_parser.parse(_params_string)
            _func_name = self.pop()

            self.push({_func_name: _params})

            self._pos = idx + 1
            self.state = 'wait_for_symbol'


    def _state_expression(self, idx):
        if self._pos == idx:
            c = self._val[idx]
            if c in '<>' and self._val[idx + 1] not in '!=<>':
                self.state = 'expession_value'
                self._stack.append(c)
                self._pos = idx + 1
        elif self._pos == idx - 1:
            c = self._val[self._pos:idx + 1]
            if c in ['!=', '==', '>=', '<=']:
                self.state = 'end'
                self._stack.append(c)
                self._pos = idx + 1
            else:
                raise InvalidTokenException('Некорректный токен `{0}`'.format(c))
