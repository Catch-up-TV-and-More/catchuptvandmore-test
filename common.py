# -*- coding: utf-8 -*-
import os
import config

ADDON_ID = "plugin.video.catchuptvandmore"
ADDON_FANART_PATHFILE = os.path.join(config.ADDON_PATH, 'fanart.jpg')
ADDON_ICON_PATHFILE = os.path.join(config.ADDON_PATH, 'icon.png')

CWD_PATH = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(CWD_PATH, 'fake_config')

CODEQUICK_PATH = os.path.join(CWD_PATH, 'script.module.codequick', 'lib')

YOUTUBE_DL_PATH = os.path.join(CWD_PATH, 'script.module.youtube.dl', 'lib')
