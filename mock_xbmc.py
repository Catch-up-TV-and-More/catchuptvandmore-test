#!/usr/bin/env python
# -*- coding: utf-8 -*-
import mock
import variables

LOGDEBUG = 0
LOGERROR = 4
LOGFATAL = 6
LOGINFO = 1
LOGNONE = 7
LOGNOTICE = 2
LOGSEVERE = 5
LOGWARNING = 3


def fake_log(msg, level=LOGDEBUG):
    if variables.ENABLE_FAKE_KODI_LOG:
        print '[FakeKodiLog] (level: ' + str(level) + ')' + msg


def fake_translate_path(path):
    return path


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
