# -*- coding: utf-8 -*-

from config import Config
from custom_logger import CustomLogger
from runtime_error import RuntimeErrorCQ

log_ = CustomLogger(__name__)

if Config.get("disable_xbmc_mock_log"):
    log_.set_log_level("ERROR")

LOGDEBUG = 0
LOGINFO = 1
LOGNOTICE = 2
LOGWARNING = 3
LOGERROR = 4
LOGSEVERE = 5
LOGFATAL = 6
LOGNONE = 7


levelno_dict = {
    0: "debug",
    1: "info",
    2: "notice",
    3: "warning",
    4: "error",
    5: "severe",
    6: "fatal",
    7: "none",
}

levelstr_dict = {
    "debug": 0,
    "info": 1,
    "notice": 2,
    "warning": 3,
    "error": 4,
    "severe": 5,
    "fatal": 6,
    "none": 6,
}


def executeJSONRPC(jsonrpccommand: str) -> str:
    """
    Execute an JSONRPC command.

    :param jsonrpccommand: string - jsonrpc command to execute.
    :return: jsonrpc return string

    List of commands -Example::

        ..
        response = xbmc.executeJSONRPC('{ "jsonrpc": "2.0", "method": "JSONRPC.Introspect", "id": 1 }')
        ..
    """
    if jsonrpccommand == ('{"method": "Settings.GetSettingValue", "params": {"setting": "network.usehttpproxy"}, '
                          '"id": 0, "jsonrpc": "2.0"}'):
        return """
        {
          "result": {
            "value": false
          }
        }
        """

    return """
        {
          "result": {}
        }
    """


def getCondVisibility(condition: str) -> bool:
    """
    Get visibility conditions

    :param condition: string - condition to check
    :return: True (1) or False (0) as a bool

    List of Conditions -http://kodi.wiki/view/List_of_Boolean_Conditions

    .. note::
        You can combine two (or more) of the above settings by
        using ``+`` as an AND operator, ``|`` as an OR operator, ``!``
        as a NOT operator, and ``[`` and ``]`` to bracket expressions.

    Example::

        ..
        visible = xbmc.getCondVisibility('[Control.IsVisible(41) + !Control.IsVisible(12)]')
        ..
    """
    return True


def log(msg, level=LOGDEBUG):
    if level >= levelstr_dict.get(Config.get("kodi_log_level"), 0):
        log_.info("[{} level] {}".format(levelno_dict.get(level, "unknown"), msg))
    RuntimeErrorCQ.last_error_message += msg
    pass


def translatePath(path):
    return path


def getInfoLabel(id_):
    if id_ == "System.BuildVersion":
        if Config.get("kodi_version") == "JARVIS":
            return "16.3 fakefakefakefakefake"
        if Config.get("kodi_version") == "KRYPTON":
            return "17.5 fakefakefakefakefake"
        if Config.get("kodi_version") == "LEIA":
            return "18.0 fakefakefakefakefake"
        if Config.get("kodi_version") == "MATRIX":
            return "19.0 fakefakefakefakefake"
        if Config.get("kodi_version") == "NEXUS":
            return "20.2 fakefakefakefakefake"
        if Config.get("kodi_version") == "OMEGA":
            return "21.0 fakefakefakefakefake"
    return ""


def getLocalizedString(id_):
    result = str(id_)
    if id_ in Config.get("xbmc_labels"):
        result = Config.get("xbmc_labels")[id_]
    log_.debug('getLocalizedString of "{}" --> "{}"'.format(id_, result))
    return result


class Keyboard(object):
    def __init__(self, line="", heading="", hidden=False):
        pass

    def doModal(self, autoclose=0):
        pass

    def getText(self):
        if Config.get("auto_exploration"):
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
