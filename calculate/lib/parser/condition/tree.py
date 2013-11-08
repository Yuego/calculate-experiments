#coding: utf-8
from __future__ import unicode_literals, absolute_import

from calculate.lib.tree import Node

import operator

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
    default = ADD

    def __add__(self, other):
        return self._combine(other, self.ADD)

    def __sub__(self, other):
        return self._combine(other, self.SUB)

    def __mul__(self, other):
        return self._combine(other, self.MUL)

    def __div__(self, other):
        return self._combine(other, self.DIV)
