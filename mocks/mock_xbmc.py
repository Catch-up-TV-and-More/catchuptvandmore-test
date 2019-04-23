# -*- coding: utf-8 -*-

import sys
import mock

from config import Config
from runtime_error import RuntimeErrorCQ

LOGDEBUG = 0
LOGERROR = 4
LOGFATAL = 6
LOGINFO = 1
LOGNONE = 7
LOGNOTICE = 2
LOGSEVERE = 5
LOGWARNING = 3


def fake_log(msg, level=LOGDEBUG):
    if not Config.get('disable_kodi_log') and level >= Config.get('kodi_log_level'):
        print('[FakeKodiLog level {}] {}'.format(level, msg))
    RuntimeErrorCQ.last_error_message += msg
    pass


def fake_translate_path(path):
    return path


def fake_get_info_label(id_):
    if id_ == 'System.BuildVersion':
        if Config.get('kodi_version') == 'JARVIS':
            return '16.3 fakefakefakefakefake'
        if Config.get('kodi_version') == 'KRYPTON':
            return '17.5 fakefakefakefakefake'
        if Config.get('kodi_version') == 'LEIA':
            return '18.0 fakefakefakefakefake'
    return ''


def get_localized_string(id_):
    result = str(id_)
    if id_ in Config.get('xbmc_labels'):
        result = Config.get('xbmc_labels')[id_]
    if not Config.get('disable_xbmc_mock_log'):
        print('[FakeXBMC] getLocalizedString of "{}" --> "{}"'.format(id_, result))
    return result


class FakeKeyboard(object):
    def __init__(self, line="", heading="", hidden=False):
        pass

    def doModal(self, autoclose=0):
        pass

    def getText(self):
        # if CONFIG['auto_exploration']:
        #     return "Chien"
        # else:
        #     try:
        #         entry = raw_input("Kodi keyboard entry: ")
        #         return entry
        #     except Exception:
        #         return ""
        return

    def isConfirmed(self):
        return True



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

mock_xbmc.Keyboard.side_effect = FakeKeyboard

# Say to Python that the xbmc module is mock_xbmc
sys.modules['xbmc'] = mock_xbmc
