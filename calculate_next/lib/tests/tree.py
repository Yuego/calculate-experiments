#coding: utf-8
from __future__ import unicode_literals, absolute_import

from unittest import TestCase

from calculate_next.lib.tree import Node

class TestTreeNode(TestCase):

    def test_init(self):
        n1 = Node()

        self.assertListEqual(n1.children, [])
        self.assertEqual(n1.connector, Node.default)
        self.assertEqual(n1.negated, False)

        n2 = Node([1, 2])
        self.assertListEqual(n2.children, [1, 2])

    def test_add_into_empty_node(self):
        n1 = Node()
        connector = 'X'

        n1.add(1, connector)
        self.assertListEqual(n1.children, [1])
        self.assertEqual(n1.connector, connector)

        n2 = Node()
        n2.add([1, 2], connector)
        self.assertListEqual(n2.children, [[1, 2]])
        self.assertEqual(n2.connector, connector)

    def test_add_into_not_empty_node(self):
        connector = 'X'
        n1 = Node([1, 2], Node.default)

        n1.add(3, Node.default)
        self.assertListEqual(n1.children, [1, 2, 3])

        n2 = Node([4, 5], Node.default)
        n1.add(n2, Node.default)
        self.assertListEqual(n1.children, [1, 2, 3, 4, 5])

        n3 = Node([6, 7], connector)
        n3.add(n2, Node.default)
        self.assertEqual(len(n3.children), 2)
        self.assertEqual(n3.children[1], n2)
        self.assertNotEqual(n3.children[0], n2)
        self.assertNotEqual(n3.children[0], n1)
        self.assertIsInstance(n2, Node)
        self.assertListEqual(n3.children[0].children, [6, 7])

    def test_negate(self):
        connector = 'X'
        n1 = Node([1, 2], connector)

        n1.negate()
        self.assertEqual(len(n1.children), 1)
        self.assertEqual(n1.connector, Node.default)
        self.assertIsInstance(n1.children[0], Node)
        self.assertListEqual(n1.children[0].children, [1, 2])
        self.assertEqual(n1.negated, not n1.children[0].negated)
