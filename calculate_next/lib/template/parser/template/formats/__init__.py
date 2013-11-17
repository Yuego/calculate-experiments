#coding: utf-8
from __future__ import unicode_literals, absolute_import

from .bind import BindFormatParser
from .compiz import CompizFormatParser
from .desktop import DesktopFormatParser
from .dhcp import DHCPFormatParser
from .dovecot import DovecotFormatParser
from .ini import INIFormatParser
from .kde import KDEFormatParser
from .openrc import OpenRCFormatParser
from .plasma import PlasmaFormatParser
from .samba import SambaFormatParser
from .squid import SquidFormatParser
from .world import WorldFormatParser

formats = {
    'ini': INIFormatParser,
}
