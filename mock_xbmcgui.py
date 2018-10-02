#!/usr/bin/env python
# -*- coding: utf-8 -*-
import mock


class FakeListItem(object):
    def __init__(self, label="", label2="", iconImage="", thumbnailImage="", path=""):
        self._label = label
        self._label2 = label2
        self._iconImage = iconImage
        self._thumbnailImage = thumbnailImage
        self._path = path
        self._property = {}
        self._info = {}
        self._art = {}

    def setLabel(self, label):
        self._label = label

    def getLabel(self):
        return self._label

    def setPath(self, path):
        self._path = path

    def getPath(self):
        return self._path

    def setProperty(self, key, value):
        self._property[key] = value

    def setInfo(self, type, infoLabels):
        self._info[type] = infoLabels

    def setArt(self, art):
        self._art = art

    def getArt(self, key):
        return self._art.get(key, '')


mock_xbmcgui = mock.MagicMock()
mock_xbmcgui.ListItem.side_effect = FakeListItem


def print_formated_listitem(listitem, is_folder, cnt):
    formated_item = ''
    if is_folder:
        formated_item += "* "
    else:
        formated_item += "- "

    formated_item += listitem.getLabel()
    formated_item += ' [' + str(cnt) + ']'

    print formated_item

    if listitem._art:
        for art_item_k, art_item_v in listitem._art.iteritems():
            print '    - [' + art_item_k + '] = ' + art_item_v

