#coding: utf-8
from __future__ import unicode_literals, absolute_import

from pyparsing import *

from calculate_next.lib.template.parser.rules import identifier, quoted_string, package_atom
from calculate_next.lib.template.parser.utils import convert_result

from calculate_next.lib.template.parser.condition.tree import *
from calculate_next.lib.registry import registry
from calculate_next.lib.version import Version
from calculate_next.lib.template.functions import functions


class ConditionParser(object):
    def __init__(self):
        self._syntax = self.get_syntax()
        # Включаем кеширование
        self._syntax.enablePackrat()

    @classmethod
    def _empty_string_atom(cls, s, l, tok):
        return ''
    @classmethod
    def _bool_atom(cls, s, l, tok):
        return tok[0].lower() in ('true', 'on', 'yes')

    @classmethod
    def _num_atom(cls, s, l, tok):
        try:
            t = int(tok[0])
        except ValueError:
            t = float(tok[0])

        return t

    @classmethod
    def _var_atom(cls, s, l, tok):
        var = tok[0]
        return registry._get_variable(var)

    @classmethod
    def _ver_atom(cls, s, l, tok):
        return Version(tok[0])

    @classmethod
    def _func_atom(cls, s, l, tok):
        fn, args = tok[0], tok[1:]
        return functions[fn](*args)

    @classmethod
    def _expr_atom(cls, s, l, tok):
        return ExpressionNode([tok[0], tok[2]], tok[1])

    @classmethod
    def _math_atom(cls, s, l, tok):
        tok = convert_result(tok)
        return MathNode(tok)

    @classmethod
    def _cond_atom(cls, s, l, tok):
        tok = convert_result(tok)

        def __process_token(t):
            while len(t) > 1:
                t[0:3] = [ConditionNode([t[0], t[2]], t[1])]
            return t[0]

        if '||' in tok:
            _and_lst = []
            while '||' in tok:
                _and_idx = tok.index('||')
                _or_tok, tok = tok[0:_and_idx], tok[_and_idx+1:]
                _and_lst.append(__process_token(_or_tok))
            _and_lst.append(__process_token(tok))
            return ConditionNode(_and_lst, ConditionNode.OR)
        return __process_token(tok)

    def parse(self, s):
        res = self._syntax.parseString(s, parseAll=True)
        return res.asList()

    def evaluate(self, s):
        return self.parse(s)[0].evaluate()

    def get_syntax(self):
        atom = Forward()
        math = Forward().setParseAction(self._math_atom)
        cond = Forward().setParseAction(self._cond_atom)
        expr = Forward().setParseAction(self._expr_atom)
        func = Forward().setParseAction(self._func_atom)

        _lpar = Suppress('(')
        _rpar = Suppress(')')
        _point = Literal('.')

        _variable = Combine(identifier + _point + identifier).setParseAction(self._var_atom)


        number = Word('+-' + nums, nums).setParseAction(self._num_atom)
        _sv = (Literal('_')
                     + (Literal('pre') | Literal('p') | Literal('beta') | Literal('alpha') | Literal('rc'))
                     + Word(nums)
        )
        _rev = (Literal('-r') + Word(nums))

        version = Combine(
            Word(nums)
            + OneOrMore(_point + Word(nums))
            + Optional(Word(alphas))
            + Optional(_sv)
            + Optional(_rev)
            ).setParseAction(self._ver_atom)

        _math_operand = _variable | number | func | Group(_lpar + math + _rpar)

        _plus = Literal('+')
        _minus = Literal('-')
        _multiply = Literal('*')
        _divide = Literal('/')
        _math_operator = (_plus | _minus | _multiply | _divide)

        math << (_math_operand + OneOrMore(_math_operator + _math_operand))

        unqouted_string = identifier


        _func_param = _variable | math | number | quoted_string | package_atom | unqouted_string | func

        func << (identifier + _lpar + Optional(
            _func_param + ZeroOrMore(Suppress(',') + _func_param)
        ) + _rpar)

        atom << (math | _variable | version | number | quoted_string | func)

        _bool = (CaselessLiteral('on') | CaselessLiteral('off')
                 | CaselessLiteral('yes') | CaselessLiteral('no')
                 | CaselessLiteral('true') | CaselessLiteral('false')
        ).setParseAction(self._bool_atom)

        _eq = Literal('==')
        _neq = Literal('!=')
        _gt = Literal('>')
        _gte = Literal('>=')
        _lt = Literal('<')
        _lte = Literal('<=')
        _expr_operator = (_eq | _neq | _gte | _lte | _gt | _lt)

        expr << (atom + _expr_operator + (atom | Empty().setParseAction(self._empty_string_atom)))

        _and = Literal('&&')
        _or = Literal('||')
        _cond_operator = (_and | _or)

        cond_atom = Group(_lpar + cond + _rpar) | expr
        cond << cond_atom + ZeroOrMore(_cond_operator + cond_atom)

        syntax = cond

        return syntax
