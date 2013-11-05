#coding: utf-8
from __future__ import unicode_literals, absolute_import

import re
import six
import sys

from calculate.lib.registry.options import Options

class ValidationErrorException(Exception):
    pass


class VariableBase(type):

    def __new__(cls, name, parents, attrs):
        super_new = super(VariableBase, cls).__new__

        # six добавляет в дерево наследования пустой класс NewBase
        # с ним ничего делать не надо
        if name == 'NewBase' and attrs == {}:
            return super_new(cls, name, parents, attrs)

        p = [p for p in parents if isinstance(p, VariableBase) and
             not (p.__name__ == 'NewBase' and p.__mro__ == (p, object))]
        if not p:
            return super_new(cls, name, parents, attrs)


        module = attrs.pop('__module__')

        new_class = super_new(cls, name, parents, {'__module__': module})

        options = attrs.pop('Options', None)

        if not options:
            opts = getattr(new_class, 'Options', None)
        else:
            opts = options

        parent_opts = getattr(new_class, '_opts', None)

        module_name = sys.modules[new_class.__module__]

        if getattr(opts, 'module', None) is None:
            m = module_name.__name__.split('.')
            opts_kwargs = {'module': m[-1], 'app': m[-3]}
        else:
            opts_kwargs = {}

        var_name = re.sub("(.)([A-Z])", "\\1_\\2", new_class.__name__[:-8]).lower()
        opts_kwargs.update({
            'name': var_name,
        })

        new_class.add_to_class('_opts', Options(opts, **opts_kwargs))

        # Единожды установленный флаг ReadOnly убрать нельзя
        if getattr(parent_opts, 'read_only', False) is True:
            new_class._opts.read_only = True

        for attr, value in attrs.items():
            new_class.add_to_class(attr, value)

        return new_class

    def add_to_class(cls, name, value):
        if hasattr(value, 'add_to_class'):
            value.add_to_class(cls, name)
        else:
            setattr(cls, name, value)

    def register_variable(cls, registry):
        setattr(getattr(registry, cls._opts.module), cls._opts.name, cls())


class Variable(six.with_metaclass(VariableBase)):
    _value = None

    def _calculate_value(self):
        """
        Метод вычисляет значение runtime-переменной
        (переменной, которая может меняться независимо от утилит, на лету)
        """
        return self._value

    def _get(self):
        """
        Метод возвращает вычисленное значение переменной

        runtime-переменная вычисляется только, если не была изменена методом _set
        """
        if self._opts.runtime and not self._opts.changed:
            return self._calculate_value()

        return self._value

    def _set(self, value, force=False):
        """
        Метод устанавливает значение переменной

        Системные (system) переменные не могут быть изменены ни при каких условиях
        ReadOnly (read_only) переменные могут быть изменены только с помощью метода set реестра
        """
        if self._opts.system:
            raise ValueError('Can`t assign System variable `{0}`'.format(self._opts.name))
        elif not force and self._opts.read_only:
            raise ValueError('Can`t assign ReadOnly variable `{0}`'.format(self._opts.name))

        self._value = self.clean(value)
        self._opts.changed = True

    def validate(self, value):
        """
        Метод проверяет корректность устанавливаемого переменной значения
        В случае непрохождения проверки бросает ValidationErrorException
        """
        pass

    def clean(self, value):
        """
        Метод приводит присваиваемое значение к необходимому виду и
        валидирует его
        """
        value = self.to_python(value)
        self.validate(value)
        return value

    def to_python(self, value):
        """
        Метод приводит тип значения к типу переменной
        """
        return value


class StringVar(Variable):

    def internal_type(self):
        return 'string'

    def short_type(self):
        return 's'

    def validate(self, value):
        super(StringVar, self).validate(value)

        if not isinstance(self._value, six.string_types):
            raise ValidationErrorException

    def to_python(self, value):
        if isinstance(value, six.string_types):
            return value

        if hasattr(value, '__unicode__'):
            value = value.__unicode__()
        else:
            if six.PY3:
                if isinstance(value, bytes):
                   value = six.text_type(value, 'utf-8', 'strict')
                else:
                    value = six.text_type(value)
            else:
                value = six.text_type(bytes(value), 'utf-8', 'strict')

        return value


class IntegerVar(Variable):

    def internal_type(self):
        return 'int'

    def short_type(self):
        return 'i'

    def validate(self, value):
        super(IntegerVar, self).validate(value)

        if not isinstance(value, six.integer_types):
            raise ValidationErrorException

    def to_python(self, value):
        return int(value)


class BooleanVar(Variable):

    def internal_type(self):
        return 'bool'

    def short_type(self):
        return 'b'

    def validate(self, value):
        super(BooleanVar, self).validate(value)

        if not isinstance(value, bool):
            raise ValidationErrorException

    def to_python(self, value):
        return bool(value)
