#coding: utf-8
from __future__ import unicode_literals, absolute_import

from pyparsing import *

from calculate.lib.parser.parser import SyntaxParser

from calculate.lib.parser.condition.tree import *
from calculate.lib.registry import registry


def __convert_result(res):
    if isinstance(res, ParseResults):
        return res.asList()[0]
    return res


def _num_atom(s, l, tok):
    try:
        t = int(tok[0])
    except ValueError:
        t = float(tok[0])

    return t


def _var_atom(s, l, tok):
    var = tok[0]
    return registry[var]


def _ver_atom(s, l, tok):
    pass


def _func_atom(s, l, tok):
    t = tok[0]
    fn = t[0]
    args = ','.join(map(lambda x: str(x), t[1:]))
    return '{0}: {1}'.format(fn, args)


def _expr_atom(s, l, tok):
    _op = {
        '==': operator.eq,
        '!=': operator.ne,
        '>': operator.gt,
        '>=': operator.ge,
        '<': operator.lt,
        '<=': operator.le,
    }

    node = ExpressionNode([tok[0], tok[2]], tok[1])

    if len(tok) > 3:
        token = tok[3:]
        for i in range(len(token)/2):
            node = _op[token[i*2]](node, token[i*2+1])
    return node


def _math_atom(s, l, tok):
    _op = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.div,
        #'^': operator.pow,
    }
    _op_priority = (
        #{'^'},
        {'*', '/'},
        {'+', '-'},
    )
    tok = map(__convert_result, tok)

    for oset in _op_priority:
        for op in oset & set(tok):
            _op_idx = tok.index(op)
            tok[_op_idx-1:_op_idx+2] = [_op[tok[_op_idx]](tok[_op_idx-1], tok[_op_idx+1])]

    return tok[0]


def _cond_atom(s, l, tok):
    tok = map(__convert_result, tok)

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

        _identifier = Word(alphas + '_', alphanums + '_')
        _variable = Combine(_identifier + _point + _identifier).setParseAction(_var_atom)


        number = Word('+-' + nums, nums).setParseAction(_num_atom)
        version = Combine(Word('+-' + nums, nums) + ZeroOrMore(_point + Word(nums))).setParseAction(_ver_atom)

        _math_operand = _variable | number | version | func | Group(_lpar + math + _rpar)

        _plus = Literal('+')
        _minus = Literal('-')
        _multiply = Literal('*')
        _divide = Literal('/')
        _math_operator = (_plus | _minus | _multiply | _divide)

        math << (_math_operand + OneOrMore(_math_operator + _math_operand))


        quoted_string = (
            QuotedString('"', escChar='\\', unquoteResults=True) | QuotedString("'", escChar='\\', unquoteResults=True)
        )
        unqouted_string = _identifier

        _func_param = atom | unqouted_string

        func << (_identifier + _lpar + Optional(
            _func_param + ZeroOrMore(Suppress(',') + _func_param)
        ) + _rpar)

        atom << (math | number | _variable | quoted_string | func)


        _eq = Literal('==')
        _neq = Literal('!=')
        _gt = Literal('>')
        _gte = Literal('>=')
        _lt = Literal('<')
        _lte = Literal('<=')
        _expr_operator = (_eq | _neq | _gte | _lte | _gt | _lt)

        expr << (atom + _expr_operator + atom)

        _and = Literal('&&')
        _or = Literal('||')
        _cond_operator = (_and | _or)

        cond_atom = Group(_lpar + cond + _rpar) | expr
        cond << cond_atom + ZeroOrMore(_cond_operator + cond_atom)

        syntax = cond

        return syntax
