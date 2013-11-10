#coding: utf-8
from __future__ import unicode_literals, absolute_import


class SyntaxParser(object):

    def __init__(self):
        self._syntax = self.get_syntax()
        # Включаем кеширование
        self._syntax.enablePackrat()

    def get_syntax(self):
        raise NotImplementedError

    def parse(self, s):
        res = self._syntax.parseString(s, parseAll=True)

        return res.asList()

    def evaluate(self, s):
        #print self.parse(s)
        return self.parse(s)[0].evaluate()
