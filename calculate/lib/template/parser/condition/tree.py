#coding: utf-8
from __future__ import unicode_literals, absolute_import

from calculate.lib.tree import Node

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
        return self._eval[self.connector](map(lambda x: x, self.children))

    def __or__(self, other):
        return self._combine(other, self.OR)

    def __and__(self, other):
        return self._combine(other, self.AND)

    def __invert__(self):
        obj = self.__class__()
        obj.add(self, self.AND)
        obj.negate()
        return obj


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
        self.negated = negated

    def evaluate(self):
        return self._eval[self.connector](*self.children)

    def _combine(self, other, connector):
        if not type(other) == self.__class__:
            return False

        obj = self.__class__(self.children)
        obj.add(other, connector)
        return obj

    def __eq__(self, other):
        return self._combine(other, self.EQ)

    def __ne__(self, other):
        return self._combine(other, self.NE)

    def __gt__(self, other):
        return self._combine(other, self.GT)

    def __ge__(self, other):
        return self._combine(other, self.GE)

    def __lt__(self, other):
        return self._combine(other, self.LT)

    def __le__(self, other):
        return self._combine(other, self.LE)

    def add(self, node, connector):
        assert len(self.children) < 2, 'Only 2 items can be compared!'

        self.connector = connector

        if isinstance(node, Node) and (node.connector == connector or len(node) == 1):
            self.children.extend(node.children)
        else:
            self.children.append(node)


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
            raise NotImplementedError
        else:
            self.children = children

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
        self.children.extend([connector, other])


    def _rcombine(self, other, connector):
        l = len(self.children)
        ret = self
        if len(self.children):
            self.children = [other, connector, self.children[0]]
        else:
            if len({self.children[1::2]}) == 1 and self.children[1] == connector:
                self.children.extend([connector, other])
            else:
                obj = MathNode([other])
                obj._combine(self, connector)
                ret = obj

        return ret

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
        return self._rcombine(other, MathNode.MUL)

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
