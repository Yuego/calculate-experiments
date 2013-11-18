#coding: utf-8
from __future__ import unicode_literals, absolute_import

from pyparsing import *
import six

from calculate_next.lib.template.parser.condition.parser import ConditionParser
from calculate_next.lib.template.parser.rules import identifier, package_atom, quoted_string
from calculate_next.lib.template.parser.utils import convert_result

_string_value = quoted_string | Word(printables)


class TemplateHeaderParser(ConditionParser):
    parameters = {
        'format': ['patch', 'raw', 'bin'],
        'append': ['join', 'before', 'after', 'replace', 'remove', 'skip', 'patch', 'clear'],
        'path': _string_value,
        'link': _string_value,
        'name': _string_value,
        'run': _string_value,
        'exec': _string_value,
        'merge': package_atom + ZeroOrMore(Suppress(',') + package_atom),
        'env': identifier,
        'chmod': Optional(Suppress('0')) + Word(nums, min=3, max=3),
        'chown': identifier + Optional(Suppress(':') + identifier),
        'comment': _string_value,
        'module': _string_value,

        'force': None,
        'mirror': None,
        'protected': None,
        'symbolic': None,
        'autoupdate': None,

        'dotall': None,
        'multiline': None,
    }

    @classmethod
    def _many_conditions_atom(cls, s, l, tok):
        if len(tok):
            return six.moves.reduce(lambda x, y: x & y, convert_result(tok))
        else:
            return []

    def get_syntax(self):
        cond = super(TemplateHeaderParser, self).get_syntax()

        if 'format' in self.parameters:
            from calculate_next.lib.template.parser.template.formats import formats
            for f in formats.keys():
                self.parameters['format'].append(f)

        prefix = Suppress('# Calculate')

        rules = []
        for key, val in self.parameters.items():
            if val is None:
                rule = Literal(key)
            else:
                if isinstance(val, (list, tuple)):
                    val_rule = six.moves.reduce(lambda x, y: x | y, map(lambda x: Literal(x), val))
                else:
                    val_rule = val

                rule = Group(Literal(key) + Suppress('=') + val_rule)
            rules.append(rule)

        params = six.moves.reduce(lambda x, y: x | y, rules)

        header = prefix + Group(ZeroOrMore(params)) + Group(ZeroOrMore(cond).setParseAction(self._many_conditions_atom))

        return header

    def parse(self, s):
        p, c = super(TemplateHeaderParser, self).parse(s)

        def _format_res(res):
            return dict(((x[0], x[1]) if isinstance(x, list) else (x, True)) for x in res)

        params = _format_res(p)
        cond = c[0] if c else True

        return params, cond

    def evaluate(self, s):
        """
        Разбирает строку заголовка и вычисляет условия.
        Если условий нет или вернулась Истина, возвращает список параметров,
        иначе возвращает None, указывая, что шаблон следует пропустить.
        """
        params, cond = self.parse(s)

        if cond:
            return params
        else:
            return None


class DirectoryHeaderParser(TemplateHeaderParser):
    parameters = {
        'append': ['join', 'remove', 'skip', 'clear'],
        'path': _string_value,
        'name': _string_value,
        'merge': package_atom + ZeroOrMore(Suppress(',') + package_atom),
        'env': identifier,
        'chmod': Optional(Suppress('0')) + Word(nums, min=3, max=3),
        'chown': identifier + Optional(Suppress(':') + identifier),

        'force': None,
        'symbolic': None,
        'autoupdate': None,
    }
