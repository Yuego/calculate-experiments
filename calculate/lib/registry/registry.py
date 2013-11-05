#coding: utf-8
from __future__ import unicode_literals, absolute_import

from importlib import import_module

from calculate.lib.registry.variable import Variable

class ModuleNotFoundException(Exception):
    pass

class VariableDescriptor(object):

    def __init__(self, var):
        self._var = var

    def __get__(self, instance, owner):
        return self._var._get()

    def __set__(self, instance, value):
        self._var._set(value)

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

    def __init__(self):
        # load default section
        self._load_section('lib')

    def __get_module(self, name):
        return self._sections.get(name, None)

    def _load_section(self, name):
        if not name in self._sections and name not in self._imported_modules:
            try:
                module = import_module('calculate.{0}.variables'.format(name))
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
                        setattr(Registry, variable_name, VariableDescriptor(variable))

                    return self._sections[section_name]
                raise ImportError('No variables in section `{0}`'.format(name))
            except ImportError as e:
                raise ModuleNotFoundException(e.message)

    def __getitem__(self, item):
        assert not isinstance(item, (int, slice)), 'Indexing isn`t supported!'

        if '.' in item:
            section, var = item.split('.', 1)
            self.__getitem__(section)
            return getattr(self, var)
        elif item in self._sections:
            return self._sections[item]
        elif hasattr(self, item):
            return getattr(self, item)
        else:
            return self._load_section(item)

    def __setitem__(self, key, value):
        raise IndexError('Module or variable can`t be defined via it`s index!')

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

            s, v = variable.split('.', 1)
            section = self.__getitem__(s)
            var = getattr(section, v)
        var._set(value, force=True)

