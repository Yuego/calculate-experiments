#coding: utf-8
from __future__ import unicode_literals, absolute_import

from importlib import import_module
import six

from calculate_next.lib.registry.variable import Variable


class ModuleNotFoundException(Exception):
    pass


class SectionDescriptor(object):

    def __set__(self, instance, value):
        raise AttributeError('Can`t write value to module')

    def __get__(self, instance, owner):
        return self


def subclass_section(name, module):
    cls_dict = {str('__module__'): module}
    return type(name, (SectionDescriptor,), cls_dict)


class Registry(object):
    _sections = {}
    _section_classes = {}
    _imported_modules = []

    def __init__(self, default_section='main', also_load=None):
        self._default_section = default_section

        # load sections
        _to_load = ['lib']
        if self._default_section != 'main':
            _to_load.append(self._default_section)
        if also_load is not None:
            if isinstance(also_load, (list, tuple)):
                _to_load.extend(also_load)
            elif isinstance(also_load, six.string_types):
                _to_load.append(also_load)
            else:
                raise ValueError('Wrong value of `also_load` attr: "{0}"'.format(also_load))
        for s in _to_load:
            self._load_section(s)

    def _load_section(self, name):
        if not name in self._sections and name not in self._imported_modules:
            try:
                module = import_module('calculate_next.{0}.variables'.format(name))
                self._imported_modules.append(name)
                section_name = getattr(module, 'section', 'main')

                vars = [v for v in dir(module) if v != 'Variable' and v.endswith('Variable')]
                if vars:
                    if section_name not in self._section_classes:
                        m = subclass_section(str(section_name.capitalize() + 'SectionDescriptor'), module.__name__)
                        self._section_classes[section_name] = m
                        self._sections[section_name] = m()
                    else:
                        m = self._section_classes[section_name]

                    for v in vars:
                        var = getattr(module, v)
                        setattr(var._opts, 'registry', self)

                        variable = var()
                        variable_name = var._opts.name

                        if hasattr(self, variable_name):
                            raise AttributeError('Variable `{0}` already defined'
                                                 'in `{1}` app!'.format(variable_name,
                                                                        variable._opts.app))

                        variable._opts.section = section_name

                        setattr(m, variable_name, variable)

                    return self._sections[section_name]
                raise ImportError('No variables in section `{0}`'.format(name))
            except ImportError as e:
                raise ModuleNotFoundException(e.message)

    def _get_variable(self, item):
        section, var = item.split('.', 1)
        if section in self._sections:
            s = self._sections[section]
        else:
            s = self._load_section(section)

        try:
            return getattr(s, var)
        except AttributeError:
            raise IndexError('Unknown variable `{0}`'.format(item))

    def __getitem__(self, item):
        assert not isinstance(item, (int, slice)), 'Indexing isn`t supported!'

        if '.' in item:
            return self._get_variable(item)._get()
        else:
            return self.__getitem__('{0}.{1}'.format(self._default_section, item))

    def __setitem__(self, key, value):
        assert not isinstance(key, (int, slice)), 'Indexing isn`t supported!'

        if '.' not in key:
            section, var = self._default_section, key
        else:
            section, var = key.split('.', 1)

        s = self._sections.get(section, self._load_section(section))
        if hasattr(s, var):
            getattr(s, var)._set(value)
        else:
            raise IndexError('Unknown variable `{0}`'.format(key))

    def set(self, variable, value):
        """
        Метод для принудительного задания значения переменной
        - игнорирует флаг read_only
        """
        if isinstance(variable, Variable):
            var = variable
        else:
            if '.' not in variable:
                raise ValueError('Variable name must contain module name')

            section, var_name = variable.split('.', 1)
            s = self._sections.get(section, self._load_section(section))

            var = getattr(s, var_name)
        var._set(value, force=True)

