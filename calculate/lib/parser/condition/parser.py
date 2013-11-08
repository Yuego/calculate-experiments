#coding: utf-8
from __future__ import unicode_literals, absolute_import

from collections import OrderedDict


from calculate.lib.parser.parser import SyntaxParser

from calculate.lib.parser.condition.syntax import condition_syntax





class ConditionParser(SyntaxParser):
    (COND_GROUP, CONDITION, COND_OPERATOR,
     EXPR_OPERATOR, EXPRESSION,
     MATH_GROUP, MATH, MATH_OPERATOR,
     FUNC, FUNC_PARAM,
     VARIABLE, STRING, NUMBER
    ) = range(13)


    _types = (
        'cond_group', 'condition', 'cond_operator',
        'expr_operator', 'expression',
        'math_group', 'math', 'math_operator',
        'function', 'func_param',
        'variable',
        'string',
        'number',
    )

    #_order = OrderedDict(zip(_types, range(len(_types))))
    _order = list(enumerate(_types))

    _state_machine = {
        0: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    }

    def parse(self, syntax):
        while(True):
            try:
                for i, t in self._order:
                    if t in syntax:
                        self._prev_state = self._state
                        self._state = self._state_machine[self._prev_state][self._types[t]]
                        self._s(t)(syntax[t])
                        break
                else:
                    raise ParseFinishedException
            except ParseFinishedException:
                break

        return self._result


    def _state_cond_group(self, group):
        group_len = len(group[0])
