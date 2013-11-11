#coding: utf-8
from __future__ import unicode_literals, absolute_import

from unittest import TestCase

from calculate.lib.template.parser.condition.tree import *


class TestConditionNode(TestCase):

    def test_or_and(self):
        n1 = ConditionNode([True])
        n2 = ConditionNode([False])

        n3 = n1 | n2
        self.assertIsInstance(n3, ConditionNode)
        self.assertNotEqual(n3, n1)
        self.assertNotEqual(n3, n2)
        self.assertListEqual(n3.children, [True, False])
        self.assertEqual(n3.connector, ConditionNode.OR)

        n4 = n2 & n1
        self.assertIsInstance(n4, ConditionNode)
        self.assertNotEqual(n4, n1)
        self.assertNotEqual(n4, n2)
        self.assertListEqual(n4.children, [False, True])
        self.assertEqual(n4.connector, ConditionNode.AND)

    def test_evaluate(self):
        true_n = ConditionNode([True])
        false_n = ConditionNode([False])

        n1 = true_n | false_n
        n2 = true_n & false_n
        self.assertEqual(n1.evaluate(), True)
        self.assertEqual(n2.evaluate(), False)

    def test_invert(self):
        n1 = ConditionNode([True, False], ConditionNode.OR)
        n2 = ConditionNode([True, False], ConditionNode.AND)

        self.assertEqual(n1.evaluate(), True)
        self.assertEqual(n2.evaluate(), False)

        not_n1 = ~n1
        not_n2 = ~n2
        self.assertEqual(not_n1.evaluate(), False)
        self.assertEqual(not_n2.evaluate(), True)


class TestExpressionNode(TestCase):

    def test_init(self):
        n1 = ExpressionNode(1)
        self.assertListEqual(n1.children, [1])
        self.assertEqual(n1.connector, ExpressionNode.EQ)

        n2 = ExpressionNode([1, 2], ExpressionNode.NE)
        self.assertListEqual(n2.children, [1, 2])
        self.assertEqual(n2.connector, ExpressionNode.NE)

        self.assertRaises(ValueError, ExpressionNode, *([1, 2, 3],))

    def test_operations(self):
        n1 = ExpressionNode(1)
        n2 = ExpressionNode(2)

        def _compare(n, connector):
            self.assertIsInstance(n, ExpressionNode)
            self.assertNotEqual(id(n), id(n1))
            self.assertNotEqual(id(n), id(n2))
            self.assertListEqual(n.children, [1, 2])
            self.assertEqual(n.connector, connector)

        n3 = n1 == n2
        _compare(n3, ExpressionNode.EQ)
        self.assertFalse(n3.evaluate())

        n4 = n1 != n2
        _compare(n4, ExpressionNode.NE)
        self.assertTrue(n4.evaluate())

        n5 = n1 > n2
        _compare(n5, ExpressionNode.GT)
        self.assertFalse(n5.evaluate())

        n6 = n1 >= n2
        _compare(n6, ExpressionNode.GE)
        self.assertFalse(n6.evaluate())

        n7 = n1 < n2
        _compare(n7, ExpressionNode.LT)
        self.assertTrue(n7.evaluate())

        n8 = n1 <= n2
        _compare(n8, ExpressionNode.LE)
        self.assertTrue(n8.evaluate())


class TestMathNode(TestCase):

    def test_operations(self):
        n0 = MathNode(1)

        def _compare(n, connector):
            self.assertNotEqual(id(n0), id(n))
            self.assertEqual(n.children, [1, connector, 5])

        def _rcompare(n, connector):
            self.assertNotEqual(id(n0), id(n))
            self.assertEqual(n.children, [5, connector, 1])

        n1 = n0 + 5
        _compare(n1, MathNode.ADD)

        n2 = n0 - 5
        _compare(n2, MathNode.SUB)

        n3 = n0 * 5
        _compare(n3, MathNode.MUL)

        n4 = n0 / 5
        _compare(n4, MathNode.DIV)

        n5 = 5 + n0
        _rcompare(n5, MathNode.ADD)

        n6 = 5 - n0
        _rcompare(n6, MathNode.SUB)

        n7 = 5 * n0
        _rcompare(n7, MathNode.MUL)

        n8 = 5 / n0
        _rcompare(n8, MathNode.DIV)
