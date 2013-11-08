#coding: utf-8
from __future__ import unicode_literals, absolute_import

from calculate.lib.tree import Node

import operator

class ConditionNode(Node):

    AND = operator.and_
    OR = operator.or_


class ExpressionNode(Node):

    EQ = operator.eq
    NEQ = operator.ne
    GT = operator.gt
    GTE = operator.ge
    LT = operator.lt
    LTE = operator.le


class MathNode(Node):

    ADD = operator.add
    SUB = operator.sub
    MUL = operator.mul
    DIV = operator.div
