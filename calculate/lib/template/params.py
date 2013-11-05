#coding: utf-8
from __future__ import unicode_literals, absolute_import

class ParameterValidationError(Exception):
    pass

class TemplateParameter(object):

    def __init__(self, value):
        self.value = value

    def validate(self):
        raise NotImplementedError

    def __str__(self):
        return str(self.__unicode__())

    def __unicode__(self):
        return '{0}({1})'.format(self.__class__.__name__[:-9].lower(), self.value)

    def __repr__(self):
        return self.__str__()

class ChoiceParameter(TemplateParameter):
    choices = []

    def validate(self):
        if self.value not in self.choices:
            raise ParameterValidationError('Недопустимое значение параметра: {0}'.format(self.value))

class BooleanParameter(TemplateParameter):
    pass

class StringParameter(TemplateParameter):

    def validate(self):
        if not self.value:
            raise ParameterValidationError('Значение параметра не может быть пустым!')

class VersionParameter(StringParameter):
    pass
    #TODO: реализовать


class FlagParameter(TemplateParameter):
    pass


class FormatParameter(ChoiceParameter):
    choices = [
        'raw', 'bin', 'diff',
    ]

class AppendParameter(ChoiceParameter):
    choices = [
        'merge', 'skip', 'append',
    ]

parameters = {
    'dotall': FlagParameter,
    'format': FormatParameter,
    'multiline': FlagParameter,
    'comment': StringParameter,
    'append': AppendParameter,
    'force': FlagParameter,
    'mirror': FlagParameter,
    'chmod': StringParameter,
    'chown': StringParameter,
    'path': StringParameter,
    'link': StringParameter,
}
