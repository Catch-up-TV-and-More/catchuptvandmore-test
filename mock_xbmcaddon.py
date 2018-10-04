# -*- coding: utf-8 -*-
import sys
import mock
import common
import config


class FakeAddon(object):
    def __init__(self, id_=common.ADDON_ID):
        self._id = id_
        self._settings = config.FAKE_SETTINGS
        self._labels = config.FAKE_LABELS

    def getAddonInfo(self, info_id):
        result = ''
        if info_id == 'id':
            result = self._id
        elif info_id == 'name':
            result = 'Catch-up TV & More'
        elif info_id == 'path':
            result = config.ADDON_PATH
        elif info_id == 'fanart':
            result = common.ADDON_FANART_PATHFILE
        elif info_id == 'icon':
            result = common.ADDON_ICON_PATHFILE
        elif info_id == 'profile':
            result = common.CONFIG_PATH
        else:
            raise Exception(
                'Need to complete getAddonInfo mock for info_id: ' + info_id)

        if config.ENABLE_MOCK_XBMCADDON_LOG:
            print('[FakeAddon] getAddonInfo of "' + info_id + '" --> "' + result + '"')
        return result

    def getSetting(self, setting_id):
        if config.ENABLE_MOCK_XBMCADDON_LOG:
            print('[FakeAddon] getSetting of "' + setting_id + '" --> "' + self._settings.get(setting_id, '') + '"')
        return self._settings.get(setting_id, '')

    def setSetting(self, _id, value):
        if config.ENABLE_MOCK_XBMCADDON_LOG:
            print('[FakeAddon] setSetting of "' + _id + '" --> "' + value + '"')
        self._settings[_id] = value

    def getLocalizedString(self, id_):
        if config.ENABLE_MOCK_XBMCADDON_LOG:
            print('[FakeAddon] getLocalizedString of ' + str(id_) + ' --> "' + self._labels.get(id_, str(id_)) + '"')
        return self._labels.get(id_, str(id_))



mock_xbmcaddon = mock.MagicMock()

mock_xbmcaddon.Addon.side_effect = FakeAddon

# Say to Python that the xbmcaddon module is mock_xbmcaddon
sys.modules['xbmcaddon'] = mock_xbmcaddon
