# -*- coding: utf-8 -*-

# The unicode_literals import only has
# an effect on Python 2.
# It makes string literals as unicode like in Python 3
from __future__ import unicode_literals


import sys
import mock
import config

LOGDEBUG = 0
LOGERROR = 4
LOGFATAL = 6
LOGINFO = 1
LOGNONE = 7
LOGNOTICE = 2
LOGSEVERE = 5
LOGWARNING = 3


def fake_log(msg, level=LOGDEBUG):
    if config.ENABLE_FAKE_KODI_LOG and level >= config.KODI_LOG_MIN_LEVEL:
        print('[FakeKodiLog level ' + str(level) + '] ' + msg)


def fake_translate_path(path):
    return path


def get_localized_string(id_):
    result = str(id_)
    if id_ in config.ADDON_FAKE_LABELS:
        result = config.ADDON_FAKE_LABELS[id_]
    elif id_ in config.CODEQUICK_FAKE_LABELS:
        result = config.CODEQUICK_FAKE_LABELS[id_]
    if config.ENABLE_MOCK_XBMC_LOG:
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

# Say to Python that the xbmc module is mock_xbmc
sys.modules['xbmc'] = mock_xbmc
