# -*- coding: utf-8 -*-

import sys
import mock
from config import *

LOGDEBUG = 0
LOGERROR = 4
LOGFATAL = 6
LOGINFO = 1
LOGNONE = 7
LOGNOTICE = 2
LOGSEVERE = 5
LOGWARNING = 3


def fake_log(msg, level=LOGDEBUG):
    if not CONFIG['disable_kodi_log'] and level >= CONFIG['kodi_log_level']:
        print('[FakeKodiLog level ' + str(level) + '] ' + msg)


def fake_translate_path(path):
    return path


def fake_get_info_label(id_):
    if id_ == 'System.BuildVersion':
        if CONFIG['kodi_version'] == 'JARVIS':
            return '16.3 fakefakefakefakefake'
        if CONFIG['kodi_version'] == 'KRYPTON':
            return '17.5 fakefakefakefakefake'
        if CONFIG['kodi_version'] == 'LEIA':
            return '18.0 fakefakefakefakefake'
    return ''


def get_localized_string(id_):
    result = str(id_)
    if id_ in ADDON_FAKE_LABELS:
        result = ADDON_FAKE_LABELS[id_]
    elif id_ in CODEQUICK_FAKE_LABELS:
        result = CODEQUICK_FAKE_LABELS[id_]
    if not CONFIG['disable_xbmc_mock_log']:
        print('[FakeAddon] getLocalizedString of ' + str(id_) + ' --> "' + result + '"')
    return result


mock_xbmc = mock.MagicMock()

mock_xbmc.log.side_effect = fake_log

mock_xbmc.LOGDEBUG = LOGDEBUG
mock_xbmc.LOGERROR = LOGERROR
mock_xbmc.LOGFATAL = LOGFATAL
mock_xbmc.LOGINFO = LOGINFO
mock_xbmc.LOGNONE = LOGNONE
mock_xbmc.LOGNOTICE = LOGNOTICE
mock_xbmc.LOGSEVERE = LOGSEVERE
mock_xbmc.LOGWARNING = LOGWARNING

mock_xbmc.translatePath.side_effect = fake_translate_path
mock_xbmc.getLocalizedString.side_effect = get_localized_string
mock_xbmc.getInfoLabel.side_effect = fake_get_info_label

# Say to Python that the xbmc module is mock_xbmc
sys.modules['xbmc'] = mock_xbmc
