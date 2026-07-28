# -*- coding: utf-8 -*-

import sys

class Window(object):
    def __init__(self, existingWindowId=-1):
        # type: (int) -> None
        self.dict = {
            'cutv_labels__labels': None
        }

    def setProperty(self, key, value):
        self.dict[key] = value

    def getProperty(self, key):
        return self.dict[key]

    def clearProperty(self, key):
        # type: (str) -> None
        pass


class ListItem(object):
    def __init__(self, label="", label2="", iconImage="", thumbnailImage="", path=""):
        self._label = label
        self._label2 = label2
        self._iconImage = iconImage
        self._thumbnailImage = thumbnailImage
        self._path = path
        self._property = {}
        self._info = {}
        self._art = {}
        self._actors = {}
        self._stream = {}
        self._context_menu = []

    def getLabel(self):
        return self._label

    def setLabel(self, label):
        self._label = label

    def getLabel2(self):
        return self._label2

    def setLabel2(self, label):
        self._label2 = label

    def getPath(self):
        return self._path

    def setPath(self, path):
        self._path = path

    def setArt(self, art):
        self._art = art

    def getArt(self, key):
        return self._art.get(key, '')

    def setInfo(self, ctype, infoLabels):
        self._info[ctype] = infoLabels

    def setCast(self, actors):
        self._actors = actors

    def addStreamInfo(self, cType, dictionary):
        self._stream[cType] = dictionary

    def setProperty(self, key, value):
        self._property[key] = value

    def getProperty(self, key):
        return self._property.get(key, '')

    def addContextMenuItems(self, items, replaceItems=False):
        self._context_menu = items

    def setContentLookup(self, enable):
        pass


class Dialog(object):
    
    def __init__(self):
        # type: () -> None
        pass
    
    def yesno(self, heading, line1, line2="", line3="", nolabel="", yeslabel="", autoclose=0):
        return True
    
    def info(self, item):
        return True
    
    def select(self, heading, list, autoclose=0, preselect=-1, useDetails=False):
        return 0
    
    def contextmenu(self, list):
        return 0
    
    def multiselect(self, heading, options, autoclose=0, preselect=None, useDetails=False):
        return [0]
    
    def ok(self, heading, line1, line2="", line3=""):
        return True
    
    def textviewer(self, heading, text, usemono=False):
        pass
    
    def browse(self, type, heading, shares, mask="", useThumbs=False, treatAsFolder=False, defaultt="", enableMultiple=False):
        return ""
    
    def browseSingle(self, type, heading, shares, mask="", useThumbs=False, treatAsFolder=False, defaultt=""):
        return ""
    
    def browseMultiple(self, type, heading, shares, mask="", useThumbs=False, treatAsFolder=False, defaultt=""):
        return [""]
    
    def numeric(self, type, heading, defaultt=""):
        return ""
    
    def notification(self, heading, message, icon="", time=0, sound=True):
        pass
    
    def input(self, heading, defaultt="", type=0, option=0, autoclose=0):
        return ""


class DialogProgress(object):
    
    def __init__(self):
        pass
    
    def create(self, heading, line1="", line2="", line3=""):
        pass
    
    def update(self, percent, line1="", line2="", line3=""):
        pass
    
    def close(self):
        pass
    
    def iscanceled(self):
        return True


class DialogProgressBG(object):
    def __init__(self):
        pass


# INT_MAX = sys.maxint
INT_MAX = 9223372036854775807


class WindowXML(Window):
    def __init__(self, xmlFilename, scriptPath, defaultSkin="Default", defaultRes="720p", isMedia=False):
        pass
    
    def addItem(self, item, position=INT_MAX):
        pass
    
    def addItems(self, items):
        pass
    
    def removeItem(self, position):
        pass
    
    def getCurrentListPosition(self):
        return 0
    
    def setCurrentListPosition(self, position):
        pass
    
    def getListItem(self, position):
        return ListItem()
    
    def getListSize(self):
        return 0
    
    def clearList(self):
        pass
    
    def setContainerProperty(self, strProperty, strValue):
        pass
    
    def setContent(self, strValue):
        pass
    
    def getCurrentContainerId(self):
        return 0
    

class WindowXMLDialog(WindowXML):
    def __init__(self, xmlFilename, scriptPath, defaultSkin="Default", defaultRes="720p"):
        pass
