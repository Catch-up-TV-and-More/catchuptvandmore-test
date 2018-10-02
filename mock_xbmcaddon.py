#!/usr/bin/env python
# -*- coding: utf-8 -*-
import mock
import variables


class FakeAddon(object):
    def __init__(self, id_=variables.ADDON_ID):
        self._id = id_
        self._settings = variables.FAKE_SETTINGS
        self._labels = variables.FAKE_LABELS

    def getAddonInfo(self, info_id):
        if info_id == 'id':
            return self._id
        elif info_id == 'name':
            return 'Catch-up TV & More'
        elif info_id == 'path':
            return variables.ADDON_PATH
        elif info_id == 'fanart':
            return variables.ADDON_FANART_PATHFILE
        elif info_id == 'icon':
            return variables.ADDON_ICON_PATHFILE
        elif info_id == 'profile':
            return variables.CONFIG_PATH
        else:
            raise Exception(
                'Need to complete getAddonInfo mock for info_id: ' + info_id)

    def getSetting(self, setting_id):
        print '[FakeAddon] getSetting of "' + setting_id + '" --> "' + self._settings.get(setting_id, '') + '"'
        return self._settings.get(setting_id, '')

    def setSetting(self, _id, value):
        print '[FakeAddon] setSetting of "' + _id + '" --> "' + value + '"'
        self._settings[_id] = value

    def getLocalizedString(self, id_):
        print '[FakeAddon] getLocalizedString of ' + str(id_) + ' --> "' + self._labels.get(id_, str(id_)) + '"'
        return self._labels.get(id_, str(id_))


mock_xbmcaddon = mock.MagicMock()
mock_xbmcaddon.Addon.side_effect = FakeAddon
