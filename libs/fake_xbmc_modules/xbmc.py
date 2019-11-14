# -*- coding: utf-8 -*-

from config import Config
from custom_logger import CustomLogger
from runtime_error import RuntimeErrorCQ

log_ = CustomLogger(__name__)

if Config.get('disable_xbmc_mock_log'):
    log_.set_log_level('ERROR')

LOGDEBUG = 0
LOGERROR = 4
LOGFATAL = 6
LOGINFO = 1
LOGNONE = 7
LOGNOTICE = 2
LOGSEVERE = 5
LOGWARNING = 3


def log(msg, level=LOGDEBUG):
    if level >= Config.get('kodi_log_level'):
        log_.info('[level {}] {}'.format(level, msg))
    RuntimeErrorCQ.last_error_message += msg
    pass


def translatePath(path):
    return path


def getInfoLabel(id_):
    if id_ == 'System.BuildVersion':
        if Config.get('kodi_version') == 'JARVIS':
            return '16.3 fakefakefakefakefake'
        if Config.get('kodi_version') == 'KRYPTON':
            return '17.5 fakefakefakefakefake'
        if Config.get('kodi_version') == 'LEIA':
            return '18.0 fakefakefakefakefake'
    return ''


def getLocalizedString(id_):
    result = str(id_)
    if id_ in Config.get('xbmc_labels'):
        result = Config.get('xbmc_labels')[id_]
    log_.debug('getLocalizedString of "{}" --> "{}"'.format(id_, result))
    return result


class Keyboard(object):
    def __init__(self, line="", heading="", hidden=False):
        pass

    def doModal(self, autoclose=0):
        pass

    def getText(self):
        if Config.get('auto_exploration'):
            return "Chien"
        else:
            entry = input("Kodi keyboard entry: ")
            return entry

    def isConfirmed(self):
        return True


class PlayList(object):
    
    def __init__(self, playList):
        # type: (int) -> None
        pass
    
    def getPlayListId(self):
        return 0
    
    def add(self, url, listitem=None, index=-1):
        pass
    
    def load(self, filename):
        return True
    
    def remove(self, filename):
        pass
    
    def clear(self):
        pass
    
    def size(self):
        return 0
    
    def shuffle(self):
        pass
    
    def unshuffle(self):
        pass
    
    def getposition(self):
        return 0


DRIVE_NOT_READY = 1
ENGLISH_NAME = 2
ISO_639_1 = 0
ISO_639_2 = 1
LOGDEBUG = 0
LOGERROR = 4
LOGFATAL = 6
LOGINFO = 1
LOGNONE = 7
LOGNOTICE = 2
LOGSEVERE = 5
LOGWARNING = 3
PLAYLIST_MUSIC = 0
PLAYLIST_VIDEO = 1
SERVER_AIRPLAYSERVER = 2
SERVER_EVENTSERVER = 6
SERVER_JSONRPCSERVER = 3
SERVER_UPNPRENDERER = 4
SERVER_UPNPSERVER = 5
SERVER_WEBSERVER = 1
SERVER_ZEROCONF = 7
TRAY_CLOSED_MEDIA_PRESENT = 96
TRAY_CLOSED_NO_MEDIA = 64
TRAY_OPEN = 16

