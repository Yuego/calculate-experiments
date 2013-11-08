#coding: utf-8
from __future__ import unicode_literals, absolute_import

import string

_name_chars = string.ascii_lowercase + string.digits

class UnexpectedSymbolException(Exception):
    pass

class InvalidTokenException(Exception):
    pass

'''
    Символы:
    a-z, 0-9, _         : literal
    _                   : underscore
    (, )                : bracket
    !, &, |             : condition
    <, >, !, =          : expression
    +, -, *, /, //      : operation
    ', "                : quote
    [:space:], \t       : space
    \n, \r              : newline
    \\                  : escape

    0 - начало работы. Ожидаем пробельные символы или буквы или символ подчеркивания

'''


class Parser(object):
    """Базовый класс конечного автомата-парсера

    Типы символов:
    0 - пробел
    1 - подчеркивание
    2 - буквы латинского алфавита
    3 - цифры
    4 - одинарная или двойная кавычка
    5 - точка
    6 - запятая
    7 - решетка
    8 - круглая скобка
    9 - оператор (+, -, *, /)
    10 - выражение (=, !, <, >)
    11 - символ экранирования "\"
    12 - перевод строки (\n, \r)

    """

    # Типы символов
    #
    (SPACE,
     UNDERSCORE, LETTER, DIGIT,
     QUOTE, PERIOD, COMMA, SHARP,
     BRACKET, OPERATOR, EXPRESSION,
     ESCAPE, NEWLINE) = range(13)

    # Состояния автомата
    _states = ('begin',)

    # Таблица переходов автомата
    _state_machine = {0: (0,)}

    def _get_token(self, char):
        """Возвращает тип символа"""

        if char in ' \t':
            return Parser.SPACE
        elif char == '_':
            return Parser.UNDERSCORE
        elif char in string.ascii_lowercase:
            return Parser.LETTER
        elif char in string.digits:
            return Parser.DIGIT
        elif char in '"\'':
            return Parser.QUOTE
        elif char == ',':
            return Parser.COMMA
        elif char == '.':
            return Parser.PERIOD
        elif char == '#':
            return Parser.SHARP
        elif char in '()':
            return Parser.BRACKET
        elif char in '+-*/':
            return Parser.OPERATOR
        elif char in '!=<>':
            return Parser.EXPRESSION
        elif char == '\\':
            return Parser.ESCAPE
        elif char in '\n\r':
            return Parser.NEWLINE

    def _s(self, name):
        """Возвращает метод состояния с именем name"""
        return getattr(self, '_state_' + name)

    def __init__(self):
        self._stack = []
        self._state = 0
        self._prev_state = None

        self._tmp = []

        self._tokens = []
        self._result = None

    def push(self, value):
        self._stack.append(value)

    def pop(self, c=1):
        assert isinstance(c, int) and c > 0, 'Invalid count!'

        ret = self._stack[:c:-1]
        self._stack = self._stack[:-c]
        return ret

    def parse(self, value):
        self._stack = []

        for char in value:
            token = self._get_token(char)
            self._prev_state = self._state
            self._state = self._state_machine[self._prev_state][token]
            self._s(self._state)(token, char)

        return self._result

    def _state_begin(self, token, char):
        raise NotImplementedError

class ExpressionParser(Parser):
    """Парсер условных выражений


    variable==1
    variable=="string"
    variable>=func(arg1,arg2)
    variable + 100 < func(arg)
    (variable + 100) * 5 == 600
    "string" == variable


    Алгоритм работы автомата:
        0 - ожидаем имя переменной - запоминаем имя
        0.1 - ожидаем оператор или выражение
        0.1.1 - получили оператор. запоминаем
        0.1.2 - ожидаем следующий операнд (переменная, функция или число)
        0.1.2 - ожидаем  операнд

    """

    # Состояния автомата
    _states = ('begin',)

    # Таблица переходов автомата
    #           Литерал 0   1   2   3   4   5   6   7   8,  9,  10, 11
    #   from:          to[token]
    _state_machine = {
        0:             (0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0),
        1:             (0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0),
    }



    def _state_begin(self, token, char):
        """Ожидаем начало:

        идентификатора: _name или name
        строки: "string" или 'string'
        вложения: (something)

        """
        if token in (Parser.UNDERSCORE, Parser.LETTER):
            self._tmp.append(char)
        elif token in (Parser.SPACE, Parser.QUOTE, Parser.BRACKET):
            pass
        else:
            raise UnexpectedSymbolException()

    def _state_wait_for_identifier(self, token, char):
        if token in (Parser.UNDERSCORE, Parser.LETTER, Parser.DIGIT):
            self._tmp.append(char)
