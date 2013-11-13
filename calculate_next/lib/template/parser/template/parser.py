#coding: utf-8
from __future__ import unicode_literals, absolute_import

from collections import OrderedDict
from pyparsing import *
import re
import six


class FormatParser(object):
    """
    Разбирает шаблон или конфиг на токены,
    представляя его в виде упорядоченного массива:

    {
        section: {
            subsection: {
                subsubsection: {...},
                key: value,
                key: value,
                ...
                __comments: { index: comment, index: comment, ... },
                },
            key: value,
            key: value
            ...
            __comments: { index: comment, index: comment, ... },
            },
        key: value,
        key: value,
        ...
        __comments: { index: comment, index: comment, ... },
        },
        key: value,
        key: value,
        ...
        __comments: { index: comment, index: comment, ... },
    }


    """

    # Символ, указывающий на начало комментария
    # Либо строка с символами, разделенными запятой,
    # ограничивающими многострочный комментарий
    # Либо список перечисленных выше элементов,
    # если синтаксис позволяет несколько форматов комментариев
    comment = None

    # Отступ по-умолчанию
    indent = 0

    def __init__(self, **kwargs):

        self._template_syntax = self.get_template_syntax()
        self._original_syntax = self.get_original_syntax()

        self._comment_starts = self._get_comment_starts()

    def _comment_atom(self, s, l, t):
        """
        Обработка строки комментария
        """
        pass

    def _is_comment(self, s):
        """
        Проверяет, является ли строка комментарием
        """
        s = s.strip()
        return any(map(lambda x: s.startswith(x), self._comment_starts))

    def _get_comment_starts(self):
        """
        Возвращает список символов, с которых может начинаться строка комментария
        """
        l = []
        if isinstance(self.comment, (list, tuple)):
            for comment in self.comment:
                if ',' in comment:
                    l.append(comment.split(',')[0])
                else:
                    l.append(comment)
        else:
            l.append(self.comment)
        return l

    def _get_comment_rule(self, comment):
        """
        Возвращает правило поиска комментария,
         начинающегося с символа {comment},
         либо ограниченного с двух сторон такими символами, если они разделены запятой
        """
        if comment is None:
            return None

        elif ',' in comment:
            rule = Regex(r'{0}.*{1}'.format(*map(lambda x: re.escape(x), comment.split(','))), re.DOTALL)
        else:
            #rule = Combine(Literal(comment) + restOfLine)
            rule = Regex(r'({0}.*[\n\r])+'.format(comment))
        return rule.setParseAction(self._comment_atom)

    def get_comment_rules(self):
        """
        Возвращает правила для поиска комментариев в файле
        """
        if isinstance(self.comment, (list, tuple)):
            return six.moves.reduce(
                lambda x, y: x | y,
                map(self._get_comment_rule, self.comment))
        else:
            return self._get_comment_rule(self.comment)

    def get_calculate_header_rule(self):
        """
        Возвращает правило для нахождения служебного комментария,
        добавляемого утилитами при обработке файла шаблоном
        """
        raise NotImplementedError

    def get_template_syntax(self):
        """
        Возвращает синтаксис для разбора шаблона
        """
        raise NotImplementedError

    def get_original_syntax(self):
        """
        Возвращает синтаксис для разбора целевого файла
        """
        raise NotImplementedError

    def expand_tree(self, l):
        """
        Проводит окончательную обработку результатов работы парсера
        """
        result = OrderedDict()
        comments = OrderedDict()
        for i, val in enumerate(l):
            if isinstance(val, six.string_types):
                comments[i] = val
            else:
                result.update(val)
        result['__comments'] = comments

        return result

    def collapse_tree(self, d, indent=None, indent_comments=False, depth=0):
        """
        Преобразует словарь обратно в строку

        tab: @int
        """
        raise NotImplementedError
