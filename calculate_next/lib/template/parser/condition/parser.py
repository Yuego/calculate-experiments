#coding: utf-8
from __future__ import unicode_literals, absolute_import

from pyparsing import *

from calculate_next.lib.template.parser.parser import SyntaxParser
from calculate_next.lib.template.parser.rules import identifier, quoted_string, package_atom
from calculate_next.lib.template.parser.utils import convert_result

from calculate_next.lib.template.parser.condition.tree import *
from calculate_next.lib.registry import registry
from calculate_next.lib.version import Version
from calculate_next.lib.template.functions import functions





def _empty_string_atom(s, l, tok):
    return ''


def _bool_atom(s, l, tok):
    return tok[0].lower() in ('true', 'on', 'yes')


def _num_atom(s, l, tok):
    try:
        t = int(tok[0])
    except ValueError:
        t = float(tok[0])

    return t


def _var_atom(s, l, tok):
    var = tok[0]
    return registry._get_variable(var)


def _ver_atom(s, l, tok):
    return Version(tok[0])


def _func_atom(s, l, tok):
    fn, args = tok[0], tok[1:]
    return functions[fn](*args)

def _expr_atom(s, l, tok):
    return ExpressionNode([tok[0], tok[2]], tok[1])


def _math_atom(s, l, tok):
    tok = convert_result(tok)
    return MathNode(tok)

def _cond_atom(s, l, tok):
    tok = convert_result(tok)

    def __process_token(tok):
        while len(tok) > 1:
            tok[0:3] = [ConditionNode([tok[0], tok[2]], tok[1])]
        return tok[0]

    if '||' in tok:
        _and_lst = []
        while '||' in tok:
            _and_idx = tok.index('||')
            _or_tok, tok = tok[0:_and_idx], tok[_and_idx+1:]
            _and_lst.append(__process_token(_or_tok))
        _and_lst.append(__process_token(tok))
        return ConditionNode(_and_lst, ConditionNode.OR)
    return __process_token(tok)


class ConditionParser(SyntaxParser):

    def get_syntax(self):
        atom = Forward()
        math = Forward().setParseAction(_math_atom)
        cond = Forward().setParseAction(_cond_atom)
        expr = Forward().setParseAction(_expr_atom)
        func = Forward().setParseAction(_func_atom)

        _lpar = Suppress('(')
        _rpar = Suppress(')')
        _point = Literal('.')

        _variable = Combine(identifier + _point + identifier).setParseAction(_var_atom)


        number = Word('+-' + nums, nums).setParseAction(_num_atom)
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
            ).setParseAction(_ver_atom)

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
        ).setParseAction(_bool_atom)

        _eq = Literal('==')
        _neq = Literal('!=')
        _gt = Literal('>')
        _gte = Literal('>=')
        _lt = Literal('<')
        _lte = Literal('<=')
        _expr_operator = (_eq | _neq | _gte | _lte | _gt | _lt)

        expr << (atom + _expr_operator + (atom | Empty().setParseAction(_empty_string_atom)))

        _and = Literal('&&')
        _or = Literal('||')
        _cond_operator = (_and | _or)

        cond_atom = Group(_lpar + cond + _rpar) | expr
        cond << cond_atom + ZeroOrMore(_cond_operator + cond_atom)

        syntax = cond

        return syntax
