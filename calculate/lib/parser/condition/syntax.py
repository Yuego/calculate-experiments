#coding: utf-8
from __future__ import unicode_literals, absolute_import

from pyparsing import *
import pprint

_identifier = Word(alphas + '_', alphanums + '_')
_variable = (Suppress('#-') + _identifier + Suppress('-#')).setResultsName('variable')


def condition_syntax():
    atom = Forward()
    oper = Forward().setResultsName('math')
    cond = Forward().setResultsName('condition')
    expr = Forward().setResultsName('expression')
    func = Forward().setResultsName('function')

    _lpar = Suppress('(')
    _rpar = Suppress(')')




    _point = Literal('.')
    number = Combine(Word('+-' + nums, nums) + Optional(_point + Word(nums))).setResultsName('number')

    _operation_atom = _variable | number | func | Group(_lpar + oper + _rpar).setResultsName('math_group')

    _plus = Literal('+')
    _minus = Literal('-')
    _multiply = Literal('*')
    _divide = Literal('/')
    _math_operator = (_plus | _minus | _multiply | _divide).setResultsName('math_operator')

    oper << Group(_operation_atom + OneOrMore(_math_operator + _operation_atom))


    quoted_string = (
        QuotedString('"', escChar='\\', unquoteResults=True) | QuotedString("'", escChar='\\', unquoteResults=True)
    ).setResultsName('string')
    unqouted_string = _identifier.setResultsName('string')

    _func_param = atom | unqouted_string

    func << Group(_identifier + _lpar + Optional(
        _func_param + ZeroOrMore(Suppress(',') + _func_param).setResultsName('func_param')
    ) + _rpar).setResultsName('function')

    atom << (oper | _variable | quoted_string | func | number)


    _eq = Literal('==')
    _neq = Literal('!=')
    _gt = Literal('>')
    _gte = Literal('>=')
    _lt = Literal('<')
    _lte = Literal('<=')
    _expr_operater = (_eq | _neq | _gt | _gte | _lt | _lte).setResultsName('expr_operator')

    expr << ((atom + _expr_operater + atom) | atom)

    _and = Literal('&&')
    _or = Literal('||')
    _cond_operator = (_and | _or).setResultsName('cond_operator')

    cond_atom = Group(_lpar + cond + _rpar).setResultsName('cond_group') | expr
    cond << cond_atom + ZeroOrMore(_cond_operator + cond_atom)

    return cond


def test(s):
    stx = condition_syntax()
    stx.enablePackrat()
    r = stx.parseString(s)

    pprint.pprint(r.asDict())
    #pprint.pprint(r.asList())



if __name__ == '__main__':

    test('(1 || 2) && 3')

    #test("(#-a-# > 0 || b((#-var-# + 1)*10) != 11.6) && (c(#-var-#, param1) || 'string') || z(#-var0-#)")
