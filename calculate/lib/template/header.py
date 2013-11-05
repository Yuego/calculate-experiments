#coding: utf-8
from __future__ import unicode_literals, absolute_import

import string

from calculate.lib.template.functions import functions as f
from calculate.lib.template.params import parameters as p

class InvalidTokenException(Exception):
    pass

class InvalidFunctionException(Exception):
    pass

class InvalidHeaderException(Exception):
    pass

_name_chars = string.ascii_lowercase + '_'


class TemplateHeaderParser(object):
    registry = None

    pos = 0
    stack = []

    def __init__(self):
        self.value = None
        self.state = None
        self.options = {}
        self.expressions = []

        self.states = {
            'begin': self._state_begin,
            'token_name': self._state_token_name,
            'param_value': self._state_param_value,
            'param_value_string': self._state_param_value_string,

            'func_param': self._state_func_param,
            'expression': self._state_expression,
            'expression_value': self._state_expression_value,
            'expression_operation': self._state_expression_operation,
        }

    def _state_begin(self, idx):
        c = self.value[idx]
        if c in [' ', '\t']:
            self.pos = idx + 1
        elif c in _name_chars:
            self.state = 'token_name'
        else:
            raise InvalidHeaderException('Неожиданный символ `{0}` в позиции {1}!'.format(c, idx))

    def _state_token_name(self, idx):
        c = self.value[idx]
        if c.lower() in _name_chars:
            return
        elif c == '=':
            self.state = 'param_value'
            self.stack.append(self.value[self.pos:idx])
            self.pos = idx + 1
        elif c == '(':
            _func_name = self.value[self.pos:idx]
            if _func_name not in f:
                raise InvalidFunctionException('Неизвестная функция `{0}`!'.format(_func_name))
            self.state = 'func_param'
            self.stack.append(f[_func_name])
            self.pos = idx + 1
        elif c in ' \t':
            self.state = 'begin'
            self.options[self.value[self.pos:idx]] = True
            self.pos = idx + 1
        else:
            raise InvalidHeaderException('Неожиданный символ `{0}` в позиции {1}!'.format(c, idx))

    def _state_param_value(self, idx):
        c = self.value[idx]
        if c in '"\'':
            if self.pos != idx:
                raise InvalidTokenException('Неожиданный символ `{0}` в позиции {1}!'.format(c, idx))
            self.state = 'param_value_string'
            self.stack.append(c)
        elif c == '=' and self.pos == idx:
            self.state = 'expression_value'
            self.stack.append(self.value[self.pos - 1:idx + 1])
            self.pos = idx + 1
        elif c in [' ', '\n']:
            self.state = 'begin'
            self.options[self.stack.pop()] = self.value[self.pos:idx].strip(' "\'')
            self.pos = idx + 1

    def _state_param_value_string(self, idx):
        c = self.value[idx]
        if c in '"\'':
            _opener = self.stack.pop()
            if c != _opener:
                raise InvalidTokenException('Открывающая кавычка не соответствует закрывающей в позиции {0}'.format(idx))
            self.state = 'param_value'
        elif c == '\n':
            raise InvalidHeaderException('Неожиданный конец строки! Возможно, пропущена кавычка после `{0}`'.format(self.value[self.pos:5]))

    def _state_func_param(self, idx):
        c = self.value[idx]
        if c == ')':
            self.state = 'expression'
            _func = self.stack.pop()
            #self.stack.append({func_name: self.value[self.pos:idx]})
            self.stack.append(_func(self.value[self.pos:idx]))
            self.pos = idx + 1
        elif c in ['(', '\n']:
            raise InvalidHeaderException('Неожиданный символ `{0}` в позиции {1}!'.format(c, idx))

    def _state_expression(self, idx):
        if self.pos == idx:
            c = self.value[idx]
            if c in ['<', '>'] and self.value[idx + 1] not in '!=<>':
                self.state = 'expression_value'
                self.stack.append(c)
                self.pos = idx + 1
        elif self.pos == idx - 1:
            c = self.value[self.pos:idx + 1]
            if c in ['!=', '==', '>=', '<=']:
                self.state = 'expression_value'
                self.stack.append(c)
                self.pos = idx + 1
            else:
                raise InvalidTokenException('Некорректный токен `{0}`'.format(c))
        else:
            raise InvalidTokenException('Пропущен операнд в позиции {0}'.format(idx))

    def _state_expression_value(self, idx):
        c = self.value[idx]
        if c in '&|':
            self.state = 'expression_operation'
            _operator = self.stack.pop()
            _left_operand = self.stack.pop()
            _right_operand = self.value[self.pos:idx]
            self.expressions.append([_left_operand, _operator, _right_operand])
            self.pos = idx + 1
        elif c in [' ', '\n']:
            self.state = 'begin'
            _operator = self.stack.pop()
            _left_operand = self.stack.pop()
            _right_operand = self.value[self.pos:idx]
            self.expressions.append([_left_operand, _operator, _right_operand])
            self.pos = idx + 1

    def _state_expression_operation(self, idx):
        c = self.value[self.pos - 1:idx + 1]
        if c in ['||', '&&']:
            self.state = 'token_name'
            self.expressions.append(c)
            self.pos = idx + 1
        else:
            raise InvalidTokenException('Неожиданный символ {0} в позиции {1}'.format(c, idx))

    def _state_end(self, idx):
        if self.pos != idx:
            if self.state == 'param_value':
                self.options[self.stack.pop()] = self.value[self.pos:idx].strip(' "\'')
            elif self.state == 'expression_value':
                _operator = self.stack.pop()
                _left_operand = self.stack.pop()
                _right_operand = self.value[self.pos:idx]
                self.expressions.append([_left_operand, _operator, _right_operand])

    def parse(self, value):
        self.value = value
        self.state = 'begin'

        for i in range(len(self.value)):
            self.states.get(self.state)(i)

        self._state_end(len(self.value))

    def validate_parameters(self):
        pass
