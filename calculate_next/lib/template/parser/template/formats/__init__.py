#coding: utf-8
from __future__ import unicode_literals, absolute_import

from .bind import BindFormatParser
from .dhcp import DHCPFormatParser
from .ini import INIFormatParser
from .openrc import OpenRCFormatParser
from .plasma import PlasmaFormatParser
from .samba import SambaFormatParser

formats = {
    'ini': INIFormatParser,
}
