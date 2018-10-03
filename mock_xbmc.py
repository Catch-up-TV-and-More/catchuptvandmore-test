# -*- coding: utf-8 -*-
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
    if config.ENABLE_FAKE_KODI_LOG:
        print('[FakeKodiLog level ' + str(level) + '] ' + msg)


def fake_translate_path(path):
    return path


def get_localized_string(id_):
    if config.ENABLE_MOCK_XBMC_LOG:
        print('[FakeAddon] getLocalizedString of ' + str(id_) + ' --> "' + config.FAKE_LABELS.get(id_, str(id_)) + '"')
    return config.FAKE_LABELS.get(id_, str(id_))


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
