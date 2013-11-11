#coding: utf-8
from __future__ import unicode_literals, absolute_import

from unittest import TestCase
import six

from calculate_next.lib.registry import registry


class TestRegistryInterface(TestCase):
    r = registry

    def test_index_interface(self):
        """
        Тестирует работу с переменными в качестве индексов массива registry
        Может быть использован в коде переменных для получения значений других
        переменных. Для присвоения значений переменным использован быть НЕ может.

        Получение значений переменных:
        value = registry['variable_name']
         - короткая запись для получения значения переменной внутри секции

        value = registry['section.variable_name']
         - полная запись. Если секция section ещё не была загружена, выполняет
         импорт секции и возвращает значение переменной


         section = registry['section']
         - возвращает дескриптор секции (если не загружена - ипортирует секцию)

         registry['section.variable_name'] = value
         - вызовет исключение.

        """
        self.assertIsInstance(self.r['cl_env_path'], six.string_types)
        self.assertIsInstance(self.r['cl_env_read_only'], six.integer_types)
        self.assertIsInstance(self.r['cl_env_flag'], bool)

        self.assertIsInstance(self.r['main.cl_env_path'], six.string_types)
        self.assertIsInstance(self.r['main.cl_env_read_only'], six.integer_types)
        self.assertIsInstance(self.r['main.cl_env_flag'], bool)

        def _func():
            return self.r['main.cl_some_var']

        self.assertRaises(IndexError, _func)

    def test_forced_variable_set(self):
        """
        Тестирует принудительное присвоение значений переменным
        """

        # Присвоить значение принудительно можно только указав полное имя переменной
        self.assertRaises(ValueError, self.r.set, *('cl_env_path', 'str'))

        # присвоение обычной переменной
        self.r.set('main.cl_env_path', '/some/path')
        self.assertEqual(self.r['cl_env_path'], '/some/path')

        # присвоение read_only-переменной
        self.r.set('main.cl_env_read_only', 50)
        self.assertEqual(self.r['cl_env_read_only'], 50)

        # а вот системной переменной значение присвоить нельзя никак
        # под системными я понимаю различные служебные переменные, которые
        # не зависят от настроек платформы, имеют фиксированные значения
        self.assertRaises(ValueError, self.r.set, *('core.cl_core_pkg_name', 'str'))

    def test_variable_validation(self):
        """
        Тестирует работу валидатора
        """

        # Строковая переменная. Может принимать любые значения, которые
        # можно сконвертировать в строку:

        class LikeString(object):
            def __unicode__(self):
                return 'like string'

        self.r['cl_env_path'] = 'str'
        self.assertEqual(self.r['cl_env_path'], 'str')

        self.r['cl_env_path'] = LikeString()
        self.assertEqual(self.r['cl_env_path'], 'like string')

        self.r['cl_env_path'] = 50
        self.assertEqual(self.r['cl_env_path'], '50')

        # Целочисленная переменная

        self.r['cl_env_number'] = 100
        self.assertEqual(self.r['cl_env_number'], 100)

        self.r['cl_env_number'] = 100.5
        self.assertEqual(self.r['cl_env_number'], 100)

        self.r['cl_env_number'] = '200'
        self.assertEqual(self.r['cl_env_number'], 200)

        def _func(value):
            self.r['cl_env_number'] = value

        self.assertRaises(ValueError, _func, *('str',))

        # Булева переменная

        self.r['cl_env_flag'] = True
        self.assertEqual(self.r['cl_env_flag'], True)

        self.r['cl_env_flag'] = 5
        self.assertEqual(self.r['cl_env_flag'], True)

        self.r['cl_env_flag'] = 'str'
        self.assertEqual(self.r['cl_env_flag'], True)

        self.r['cl_env_flag'] = object
        self.assertEqual(self.r['cl_env_flag'], True)

        self.r['cl_env_flag'] = False
        self.assertEqual(self.r['cl_env_flag'], False)

        self.r['cl_env_flag'] = None
        self.assertEqual(self.r['cl_env_flag'], False)

        self.r['cl_env_flag'] = ''
        self.assertEqual(self.r['cl_env_flag'], False)
