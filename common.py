# -*- coding: utf-8 -*-
import os
from config import CONFIG

CWD_PATH = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(CWD_PATH, 'fake_config')

ADDON_ID = "plugin.video.catchuptvandmore"
ADDON_FANART_PATHFILE = os.path.join(CONFIG['addon_path'], 'fanart.jpg')
ADDON_ICON_PATHFILE = os.path.join(CONFIG['addon_path'], 'icon.png')

CODEQUICK_PATH = os.path.join(CWD_PATH, 'script.module.codequick', 'lib')
CODEQUICK_ADDON_PATH = os.path.join(CWD_PATH, 'script.module.codequick')
CODEQUICK_FANART_PATHFILE = os.path.join(CODEQUICK_ADDON_PATH, 'fanart.jpg')
CODEQUICK_ICON_PATHFILE = os.path.join(CODEQUICK_ADDON_PATH, 'icon.png')

INPUTSTREAMHELPER_PATH = os.path.join(CWD_PATH, 'script.module.inputstreamhelper', 'lib')
INPUTSTREAMHELPER_ADDON_PATH = os.path.join(CWD_PATH, 'script.module.inputstreamhelper')
INPUTSTREAMHELPER_FANART_PATHFILE = os.path.join(INPUTSTREAMHELPER_ADDON_PATH, 'fanart.jpg')
INPUTSTREAMHELPER_ICON_PATHFILE = os.path.join(INPUTSTREAMHELPER_ADDON_PATH, 'icon.png')
