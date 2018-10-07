# -*- coding: utf-8 -*-

# The unicode_literals import only has
# an effect on Python 2.
# It makes string literals as unicode like in Python 3
from __future__ import unicode_literals


import os
import config

ADDON_ID = "plugin.video.catchuptvandmore"
ADDON_FANART_PATHFILE = os.path.join(config.ADDON_PATH, 'fanart.jpg')
ADDON_ICON_PATHFILE = os.path.join(config.ADDON_PATH, 'icon.png')

CWD_PATH = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(CWD_PATH, 'fake_config')

CODEQUICK_PATH = os.path.join(CWD_PATH, 'script.module.codequick', 'lib')
CODEQUICK_ADDON_PATH = os.path.join(CWD_PATH, 'script.module.codequick')
CODEQUICK_FANART_PATHFILE = os.path.join(CODEQUICK_ADDON_PATH, 'fanart.jpg')
CODEQUICK_ICON_PATHFILE = os.path.join(CODEQUICK_ADDON_PATH, 'icon.png')
