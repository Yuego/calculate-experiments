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
        list_section: [
            [list_section1 items],
            [list_section2 items],
            ...
            [list_sectionN items],
        ]
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

    list_section - список секций с повторяющимися именами:
    pool { <pool 1 params> }
    pool { <pool 2 params> }
    ...
    pool { <pool n params> }
    такие секции внутри себя не могут иметь вложенных секций
    только строки комметариев и параметров

    При слиянии такие секции сравниваются по содержимому.
    Две секции с хотя бы одним одинаковым параметром считаются одинаковыми:

    pool {
        allow members of "baz";
        range 10.0.30.10 10.0.30.230;
    }
    pool {
        allow members of "baz";
        range 10.0.200.20 10.0.200.50;
    }


    Стратегии слияния:
    ! :: заменить целиком (актуально только для блоков и переменных)
    - :: удалить элемент или блок
    ^ :: вставить в начало родительского блока (если уже существует - переместить в начало)
    + :: добавить в конец родительского блока (если уже существует - переместить в конец)
    """

    # Символ, указывающий на начало комментария
    # Либо строка с символами, разделенными запятой,
    # ограничивающими многострочный комментарий
    # Либо список перечисленных выше элементов,
    # если синтаксис позволяет несколько форматов комментариев
    comment = None

    # Отступ по-умолчанию
    indent = ''
    # Форматировать комментарии отступами
    indent_comments = False

    # Сортировать ли дерево после слияния
    sort_keys = False
    # На какую глубину сортировать
    sort_depth = 0

    # Стратегии слияния
    STRATS = ('!', '-', '^', '+')
    REPLACE, REMOVE, BEFORE, AFTER = STRATS

    def __init__(self, **kwargs):
        strategy = kwargs.pop('strategy', 'after')

        self._default_add_strategy = {
            'after': self.AFTER,
            'before': self.BEFORE,
        }.get(strategy, 'after')

        self._syntax = self.get_syntax()

        self._comment_starts = self._get_comment_starts()

    @classmethod
    def _comment_atom(cls, s, l, t):
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
            rule = Regex(r'[ \t]*{0}.*{1}'.format(*map(lambda x: re.escape(x), comment.split(','))), re.DOTALL)
        else:
            rule = Regex(r'[ \t]*({0}[^\n\r]*)+'.format(comment))
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

    def get_syntax(self):
        """
        Возвращает синтаксис для разбора целевого файла
        """
        raise NotImplementedError

    def expand_tree(self, l):
        """
        Проводит окончательную обработку результатов работы парсера
        """
        result = OrderedDict()
        comments = {}
        for i, val in enumerate(l):
            if isinstance(val, six.string_types):
                comments[i] = val
            else:
                result.update(val)
        result['__comments'] = comments

        return result

    def collapse_tree(self, d, depth=0):
        """
        Преобразует словарь обратно в строку
        """
        raise NotImplementedError

    def _merge(self, dst, src):
        #TODO: пересортировывать комментарии при слиянии
        for src_key in src:
            strategy = None
            if src_key == '__comments':
                continue

            if src_key[0] in self.STRATS:
                strategy = src_key[0]
                dst_key = src_key[1:]
            else:
                dst_key = src_key

            # Если ключ один для многих элементов,
            # все они содержатся в списке.
            # Списки сливаем по отдельному алгоритму
            if isinstance(src[src_key], list):
                _dst = dst[dst_key]
                _src = src[src_key]
                for s in _src:
                    if s in _dst:
                        s_idx = _dst.index(s)

                        if s.mode in (self.REMOVE, self.REPLACE, self.BEFORE):
                            _dst.pop(s_idx)
                            if s.mode == self.REPLACE:
                                _dst.insert(s_idx, s)
                            elif s.mode == self.BEFORE:
                                _dst.insert(0, s)
                        else:
                            _dst.append(s)
                    else:
                        if s.mode == self.BEFORE:
                            _dst.insert(0, s)
                        else:
                            _dst.append(s)
            # Это словарь.
            else:
                # Ключ уже есть. Сливаем по указанной стратегии
                if dst_key in dst:
                    # Стратегия удаления. Удаляем элемент неглядя
                    if strategy == self.REMOVE:
                        del dst[dst_key]
                    # Стратегия полной замены
                    elif strategy == self.REPLACE:
                        dst[dst_key] = src[src_key]
                    # Стратегия слияния
                    else:
                        # Выполняем слияние содержимого
                        if (isinstance(dst[dst_key], (dict, OrderedDict))
                            and isinstance(src[src_key], (dict, OrderedDict))):

                            new_src = self._merge(dst[dst_key], src[src_key])

                            # Слить и переместить в начало
                            if strategy == self.BEFORE:
                                del dst[dst_key]

                                new_dst = OrderedDict({
                                    dst_key: new_src
                                })
                                new_dst.update(dst)
                                dst = new_dst
                            # Слить и переместить в конец
                            elif strategy == self.AFTER:
                                comments = dst.pop('__comments')
                                del dst[dst_key]

                                new_dst = OrderedDict()
                                new_dst.update(dst)
                                new_dst[dst_key] = new_src
                                new_dst['__comments'] = comments
                                dst = new_dst
                            # Слить на месте
                            else:
                                dst[dst_key] = new_src

                        # Элементы идентичны. Ничего не делаем
                        elif dst[dst_key] == src[src_key]:
                            pass
                        # Не указана стратегия, но есть параметр с таким именем
                        # Заменяем
                        else:
                            dst[dst_key] = src[src_key]

                # Ключа нет - просто добавляем
                else:
                    if strategy is None:
                        strategy = self._default_add_strategy

                    # Добавляем в начало
                    if strategy == self.BEFORE:
                        comments = dst.pop('__comments')
                        new_dst = OrderedDict({
                            dst_key: src[src_key]
                        })
                        new_dst.update(dst)
                        new_dst['__comments'] = comments
                        dst = new_dst
                    # Добавляем в конец
                    else:
                        comments = dst.pop('__comments')
                        dst[dst_key] = src[src_key]
                        dst['__comments'] = comments
        return dst

    def _sort_keys(self, d, depth=0):
        #TODO: реализовать
        return d

    def merge(self, dst, src, path=None):
        result = self._merge(dst=dst, src=src)

        if self.sort_keys:
            result = self._sort_keys(result)

        return result

    def parse(self, content):
        return self.expand_tree(self._syntax.parseString(content, parseAll=True))
