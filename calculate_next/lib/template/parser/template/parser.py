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
    indent = 0

    # Сортировать ли дерево после слияния
    sort_keys = False
    # На какую глубину сортировать
    sort_depth = 0

    def __init__(self, **kwargs):

        self._template_syntax = self.get_template_syntax()
        self._original_syntax = self.get_syntax()

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

    def collapse_tree(self, d, indent=None, indent_comments=False, depth=0):
        """
        Преобразует словарь обратно в строку

        tab: @int
        """
        raise NotImplementedError

    def _merge(self, dst, src, path=None):
        #TODO: пересортировывать комментарии при слиянии

        if path is None:
            path = []

        for src_key in src:
            strategy = None
            if src_key == '__comments':
                continue

            if src_key[0] in ('!', '+', '-', '^'):
                strategy = src_key[0]
                dst_key = src_key[1:]
            else:
                dst_key = src_key

            # Ключ уже есть. Сливаем по указанной стратегии
            if dst_key in dst:
                # Стратегия удаления. Удаляем элемент неглядя
                if strategy == '-':
                    del dst[dst_key]
                # Стратегия полной замены
                elif strategy == '!':
                    dst[dst_key] = src[src_key]
                # Стратегия слияния
                else:
                    # Выполняем слияние содержимого
                    if (isinstance(dst[dst_key], (dict, OrderedDict))
                        and isinstance(src[src_key], (dict, OrderedDict))):

                        new_src = self._merge(dst[dst_key], src[src_key], path.append(str(dst_key)))

                        # Слить и переместить в начало
                        if strategy == '^':
                            del dst[dst_key]

                            new_dst = OrderedDict({
                                dst_key: new_src
                            })
                            new_dst.update(dst)
                            dst = new_dst
                        # Слить и переместить в конец
                        elif strategy == '+':
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
                        #path.append(str(dst_key))
                        #raise Exception('Conflict at {0}'.format('.'.join(path)))

            # Ключа нет - просто добавляем
            else:
                if strategy == '^':
                    comments = dst.pop('__comments')
                    new_dst = OrderedDict({
                        dst_key: src[src_key]
                    })
                    new_dst.update(dst)
                    new_dst['__comments'] = comments
                    dst = new_dst
                else:
                    comments = dst.pop('__comments')
                    dst[dst_key] = src[src_key]
                    dst['__comments'] = comments
        return dst

    def _sort_keys(self, d, depth=0):
        #TODO: реализовать
        return d

    def merge(self, dst, src, path=None):
        result = self._merge(dst=dst, src=src, path=path)

        if self.sort_keys:
            result = self._sort_keys(result)

        return result
