#coding: utf-8
from __future__ import unicode_literals, absolute_import

from calculate_next.lib.template.parser.template.formats import formats

_raw_formats = ('raw', 'bin')


class TemplateProcessor(object):
    """
    Производит:
    1. разбор заголовка шаблона и выбор стратегии обработки шаблона
    2. получение метаданных из целевого файла (если таковые есть)
       и принятие решения о необходимости наложения шаблона

    3. препроцессинг шаблона
    4. разбор и слияние шаблона и целевого файла
    5. добавление метаданнык в целевой файл
    6. запись файла на диск
    """

    def __init__(self, **kwargs):
        self._format = kwargs.pop('format', 'raw')
        self._parser = None
        if self._format not in _raw_formats:
            if not self._format in formats:
                raise TypeError('Unknown template format: {0}'.format(self._format))
            else:
                self._parser = formats[self._format]

        self._strategy = kwargs.pop('append', None)
        if self._strategy is None:
            if self._format in _raw_formats:
                self._strategy = 'replace'
            else:
                self._strategy = 'join'

        self._params = kwargs

    def process(self):
        pass

