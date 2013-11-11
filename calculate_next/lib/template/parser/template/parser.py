#coding: utf-8
from __future__ import unicode_literals, absolute_import

from calculate_next.lib.template.parser.parser import SyntaxParser


class FormatParser(object):



    def get_template_syntax(self):
        raise NotImplementedError

    def get_original_syntax(self):
        raise NotImplementedError

    def expand_tree(self):
        raise NotImplementedError

    def collapse_tree(self):
        raise NotImplementedError
