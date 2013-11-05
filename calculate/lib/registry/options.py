#coding: utf-8
from __future__ import unicode_literals, absolute_import

NAMES = (
    'read_only', 'hidden', 'trusted', 'system', 'runtime',
    'label', 'description',)


class Options(object):

    def __init__(self, opts, app, module, name):

        self.opts = opts
        self.app = app
        self.section = 'main'
        self.module = module
        self.name = 'cl_{0}_{1}'.format(module, name)

        self.label = ''
        self.description = ''

        self.read_only = False
        self.hidden = True
        self.trusted = True
        self.system = False
        self.runtime = False

        #Runtime options
        self.changed = False

    def add_to_class(self, cls, name):
        setattr(cls, name, self)

        # Применим опции родительского класса
        if self.opts:
            options = self.opts.__dict__.copy()

            for name in self.opts.__dict__:
                if name.startswith('_'):
                    del options[name]

            for name in NAMES:
                if name in options:
                    setattr(self, name, options.pop(name))
                elif hasattr(self.opts, name):
                    setattr(self, name, getattr(self.opts, name))

            if options != {}:
                raise TypeError("'class Options' got invalid attribute(s): %s" % ','.join(options.keys()))

        del self.opts
