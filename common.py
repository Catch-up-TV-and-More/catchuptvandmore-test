# -*- coding: utf-8 -*-
import os
import config

CWD_PATH = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(CWD_PATH, 'fake_config')

ADDON_ID = "plugin.video.catchuptvandmore"
ADDON_FANART_PATHFILE = os.path.join(config.ADDON_PATH, 'fanart.jpg')
ADDON_ICON_PATHFILE = os.path.join(config.ADDON_PATH, 'icon.png')

CODEQUICK_PATH = os.path.join(CWD_PATH, 'script.module.codequick', 'lib')
CODEQUICK_ADDON_PATH = os.path.join(CWD_PATH, 'script.module.codequick')
CODEQUICK_FANART_PATHFILE = os.path.join(CODEQUICK_ADDON_PATH, 'fanart.jpg')
CODEQUICK_ICON_PATHFILE = os.path.join(CODEQUICK_ADDON_PATH, 'icon.png')
