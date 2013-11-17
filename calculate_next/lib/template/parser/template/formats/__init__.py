#coding: utf-8
from __future__ import unicode_literals, absolute_import

from .bind import BindFormatParser
from .desktop import DesktopFormatParser
from .dhcp import DHCPFormatParser
from .ini import INIFormatParser
from .kde import KDEFormatParser
from .openrc import OpenRCFormatParser
from .plasma import PlasmaFormatParser
from .samba import SambaFormatParser
from .world import WorldFormatParser

formats = {
    'ini': INIFormatParser,
}
