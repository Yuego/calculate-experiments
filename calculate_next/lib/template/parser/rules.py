#coding: utf-8
from __future__ import unicode_literals, absolute_import

from pyparsing import (
    alphas, alphanums,
    QuotedString, Regex, Word,
)

identifier = Word(alphas + '_', alphanums + '_')

_package = r'[\w+][\w+.-]*/[\w+][\w+-]*'
_slot = r'[\w+][\w+.-]*'

package_atom = Regex(_package)
package_slot = Regex(_slot)
slotted_package_atom = Regex(_package + '(:' + _slot + ')?')

quoted_string = (
    QuotedString('"', escChar='\\', unquoteResults=True) | QuotedString("'", escChar='\\', unquoteResults=True)
)
