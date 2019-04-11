# -*- coding: utf-8 -*-
import os
import sys
import polib
from config import CONFIG
from xml.etree import ElementTree as ET

CWD_PATH = os.path.dirname(os.path.abspath(__file__))

# Fake Kodi/userdata/addon_data/plugin.video.catchuptvandmore
USERDATA_PATH = os.path.join(CWD_PATH, 'fake_userdata')

ADDON_ID = "plugin.video.catchuptvandmore"
ADDON_FANART_PATHFILE = os.path.join(CONFIG['addon_path'], 'fanart.jpg')
ADDON_ICON_PATHFILE = os.path.join(CONFIG['addon_path'], 'icon.png')

# Parse english strings.po
# in order to recover labels
# Key format: 30500
# Value format: "France"
ADDON_EN_STRINGS_PO_FILEPATH = os.path.join(CONFIG['addon_path'], "resources", "language", "resource.language.en_gb", "strings.po")
ADDON_LABELS = {}
po = polib.pofile(ADDON_EN_STRINGS_PO_FILEPATH)
for entry in po:
    key = entry.msgctxt
    key = int(key.replace('#', ''))
    ADDON_LABELS[key] = entry.msgid

# Parse settings.xml file
ADDON_SETTINGS_FILEPATH = os.path.join(CONFIG['addon_path'], "resources", "settings.xml")
ADDON_SETTINGS = {}
xml = ET.parse(ADDON_SETTINGS_FILEPATH)
for child in xml.iter():
    if child.tag == "setting":
        if 'id' in child.attrib:
            value = ''
            print(child.attrib)
            if child.attrib['type'] == 'folder':
                value = '/tmp'
            else:
                value = child.attrib['default']
            ADDON_SETTINGS[child.attrib['id']] = value


CODEQUICK_PATH = os.path.join(CWD_PATH, 'script.module.codequick', 'lib')
CODEQUICK_ADDON_PATH = os.path.join(CWD_PATH, 'script.module.codequick')
CODEQUICK_FANART_PATHFILE = os.path.join(CODEQUICK_ADDON_PATH, 'fanart.jpg')
CODEQUICK_ICON_PATHFILE = os.path.join(CODEQUICK_ADDON_PATH, 'icon.png')

INPUTSTREAMHELPER_PATH = os.path.join(CWD_PATH, 'script.module.inputstreamhelper', 'lib')
INPUTSTREAMHELPER_ADDON_PATH = os.path.join(CWD_PATH, 'script.module.inputstreamhelper')
INPUTSTREAMHELPER_FANART_PATHFILE = os.path.join(INPUTSTREAMHELPER_ADDON_PATH, 'fanart.jpg')
INPUTSTREAMHELPER_ICON_PATHFILE = os.path.join(INPUTSTREAMHELPER_ADDON_PATH, 'icon.png')


def to_unicode(s):
    if isinstance(s, str) and sys.version_info < (3, 0):
        return s.decode('utf-8')
    return s
