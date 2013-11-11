#coding: utf-8
from __future__ import unicode_literals, absolute_import


class Node(object):

    default = 'DEFAULT'

    def __init__(self, children=None, connector=None, negated=False):
        self.children = children and children[:] or []
        self.connector = connector or self.default
        self.negated = negated

    @classmethod
    def _new_instance(cls, children=None, connector=None, negated=False):

        obj = Node(children, connector, negated)
        obj.__class__ = cls
        return obj

    def __str__(self):
        if self.negated:
            return '(NOT (%s: %s))' % (self.connector, ', '.join([str(x) for x in self.children]))
        return '(%s: %s)' % (self.connector, ', '.join([str(x) for x in self.children]))

    def __repr__(self):
        return self.__str__()

    def __len__(self):
        return len(self.children)

    def __bool__(self):
        return bool(self.evaluate())

    def __nonzero__(self):
        return type(self).__bool__(self)

    def add(self, node, connector):

        if node in self.children and connector == self.connector:
            return

        if len(self.children) < 2:
            self.connector = connector

        if self.connector == connector:
            if isinstance(node, Node) and (node.connector == connector or len(node) == 1):
                self.children.extend(node.children)
            else:
                self.children.append(node)
        else:
            obj = self._new_instance(self.children, self.connector, self.negated)
            self.connector = connector
            self.children = [obj, node]

    def negate(self):
        self.children = [self._new_instance(self.children, self.connector, not self.negated)]
        self.connector = self.default

    def evaluate(self):
        raise NotImplementedError

    def _combine(self, other, connector):
        if not type(other) == self.__class__:
            raise TypeError(other)

        obj = self.__class__()
        obj.add(self, connector)
        obj.add(other, connector)
        return obj
