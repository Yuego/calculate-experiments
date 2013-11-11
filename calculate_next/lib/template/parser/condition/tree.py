#coding: utf-8
from __future__ import unicode_literals, absolute_import

from calculate_next.lib.tree import Node

import operator
import six


class ConditionNode(Node):

    AND = '&&'
    OR = '||'
    default = OR

    _eval = {
        AND: all,
        OR: any,
    }

    def evaluate(self):
        res = self._eval[self.connector](map(lambda x: x, self.children))
        if self.negated:
            res = not res
        return res

    def __or__(self, other):
        return self._combine(other, self.OR)

    def __and__(self, other):
        return self._combine(other, self.AND)

    def __invert__(self):
        self.negated = not self.negated
        return self


class ExpressionNode(Node):

    EQ = '=='
    NE = '!='
    GT = '>'
    GE = '>='
    LT = '<'
    LE = '<='
    default = EQ

    _eval = {
        EQ: operator.eq,
        NE: operator.ne,
        GT: operator.gt,
        GE: operator.ge,
        LT: operator.lt,
        LE: operator.le,
    }

    def __init__(self, children, connector=None, negated=False):
        if isinstance(children, (list, tuple)):
            if len(children) <= 2:
                self.children = children
            else:
                raise ValueError('Only 2 items can be compared!')
        else:
            self.children = [children]

        self.connector = connector or self.default
        self.negated = False

    def evaluate(self):
        return self._eval[self.connector](*self.children)

    def __and__(self, other):
        return ConditionNode([self]) & other

    def __or__(self, other):
        return ConditionNode([self]) | other


class MathNode(Node):

    ADD = '+'
    SUB = '-'
    MUL = '*'
    DIV = '/'
    #POW = '^'
    default = None

    _op = {
        ADD: operator.add,
        SUB: operator.sub,
        MUL: operator.mul,
        DIV: operator.div if six.PY2 else operator.truediv,
        #POW: operator.pow,
    }
    _op_priority = (
        #{POW},
        {MUL, DIV},
        {ADD, SUB},
    )

    def __init__(self, children, connector=None, negated=False):
        if connector is not None:
            raise ValueError('connector setting isn`t supported here')
        else:
            if isinstance(children, (list, tuple)):
                self.children = children and children[:] or []
            else:
                self.children = [children]

    def evaluate(self):
        l = self.children[:]
        _evaluate = lambda x, y: x[y].evaluate() if isinstance(x[y], MathNode) else x[y]

        for oset in self._op_priority:
            for op in oset & set(l):
                while op in l:
                    _op_idx = l.index(op)
                    l[_op_idx-1:_op_idx+2] = [self._op[l[_op_idx]](_evaluate(l, _op_idx-1), _evaluate(l, _op_idx+1))]

        return l[0]

    def __str__(self):
        return '({0})'.format(''.join(map(str, self.children)))

    def _combine(self, other, connector):
        children = self.children[:]
        children.extend([connector, other])
        return self.__class__(children)

    def _rcombine(self, other, connector):
        l = len(self.children)

        if len(self.children) == 1:
            return MathNode([other, connector, self.children[0]])
        else:
            if len({self.children[1::2]}) == 1 and self.children[1] == connector:
                children = [other, connector]
                children.extend(self.children)
                return MathNode(children)
            else:
                obj = MathNode([other])
                return obj._combine(self, connector)


    def __hash__(self):
        return hash(self.__str__())

    def __add__(self, other):
        return self._combine(other, MathNode.ADD)

    def __radd__(self, other):
        return self._rcombine(other, MathNode.ADD)

    def __sub__(self, other):
        return self._combine(other, MathNode.SUB)

    def __rsub__(self, other):
        return self._rcombine(other, MathNode.SUB)

    def __mul__(self, other):
        return self._combine(other, MathNode.MUL)

    def __rmul__(self, other):
        return self._rcombine(other, MathNode.MUL)

    def __div__(self, other):
        return self._combine(other, MathNode.DIV)

    def __rdiv__(self, other):
        return self._rcombine(other, MathNode.DIV)

    # python 3 division support
    def __truediv__(self, other):
        return self.__div__(other)

    def __rtruediv__(self, other):
        return self.__rdiv__(other)

    def __eq__(self, other):
        return self.evaluate() == other

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        return self.evaluate() > other

    def __lt__(self, other):
        return self.evaluate() < other

    def __ge__(self, other):
        return not self.__lt__(other)

    def __le__(self, other):
        return not self.__gt__(other)
