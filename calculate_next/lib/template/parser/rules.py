#coding: utf-8
from __future__ import unicode_literals, absolute_import

from pyparsing import (
    alphas, alphanums,
    QuotedString, Regex, Word,
)

identifier = Word(alphas + '_', alphanums + '_')

package_atom = Regex(r'[\w+][\w+.-]*/[\w+][\w+-]*')

quoted_string = (
    QuotedString('"', escChar='\\', unquoteResults=True) | QuotedString("'", escChar='\\', unquoteResults=True)
)
