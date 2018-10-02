#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os


# TO ADAPT
ADDON_ID = "plugin.video.catchuptvandmore"


CWD_PATH = os.path.dirname(os.path.abspath(__file__))
CODEQUICK_PATH = os.path.join(CWD_PATH, 'script.module.codequick', 'lib')

# TO ADAPT
ADDON_PATH = os.path.join(CWD_PATH, '..', 'plugin.video.catchuptvandmore')

ADDON_FANART_PATHFILE = os.path.join(ADDON_PATH, 'fanart.jpg')
ADDON_ICON_PATHFILE = os.path.join(ADDON_PATH, 'icon.png')
CONFIG_PATH = os.path.join(CWD_PATH, 'fake_config')

# TO ADAPT
FAKE_SETTINGS = {
    'live_tv': 'true',
    'live_tv.order': '1',
    'replay': 'true',
    "replay.order": '2',
    'websites': 'true',
    'websites.order': '3'
}

# TO ADAPT
FAKE_LABELS = {

}
