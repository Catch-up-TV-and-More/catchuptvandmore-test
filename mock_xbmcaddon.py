# -*- coding: utf-8 -*-

import sys
import mock
import common
from config import *

ADDONS_SETTINGS = {
    'plugin.video.catchuptvandmore': ADDON_FAKE_SETTINGS,
    'script.module.codequick': CODEQUICK_FAKE_SETTINGS,
    'script.module.inputstreamhelper': INPUTSTREAMHELPER_FAKE_SETTINGS
}

ADDONS_LABELS = {
    'plugin.video.catchuptvandmore': ADDON_FAKE_LABELS,
    'script.module.codequick': CODEQUICK_FAKE_LABELS,
    'script.module.inputstreamhelper': INPUTSTREAMHELPER_FAKE_LABELS
}

ADDONS_NAME = {
    'plugin.video.catchuptvandmore': 'Catch-up TV & More',
    'script.module.codequick': 'CodeQuick',
    'script.module.inputstreamhelper': 'InputStream Helper'
}

ADDONS_PATHS = {
    'plugin.video.catchuptvandmore': CONFIG['addon_path'],
    'script.module.codequick': common.CODEQUICK_ADDON_PATH,
    'script.module.inputstreamhelper': common.INPUTSTREAMHELPER_ADDON_PATH
}

ADDONS_FANARTS = {
    'plugin.video.catchuptvandmore': common.ADDON_FANART_PATHFILE,
    'script.module.codequick': common.CODEQUICK_FANART_PATHFILE,
    'script.module.inputstreamhelper': common.INPUTSTREAMHELPER_FANART_PATHFILE
}

ADDONS_ICONS = {
    'plugin.video.catchuptvandmore': common.ADDON_ICON_PATHFILE,
    'script.module.codequick': common.CODEQUICK_ICON_PATHFILE,
    'script.module.inputstreamhelper': common.INPUTSTREAMHELPER_ICON_PATHFILE
}


class FakeAddon(object):
    def __init__(self, id='plugin.video.catchuptvandmore'):
        self._id = id
        self._settings = ADDONS_SETTINGS[self._id]
        self._labels = ADDONS_LABELS[self._id]
        self._name = ADDONS_NAME[self._id]
        self._path = ADDONS_PATHS[self._id]
        self._fanart = ADDONS_FANARTS[self._id]
        self._icon = ADDONS_ICONS[self._id]

    def getAddonInfo(self, info_id):
        result = ''
        if info_id == 'id':
            result = self._id
        elif info_id == 'name':
            result = self._name
        elif info_id == 'path':
            result = self._path
        elif info_id == 'fanart':
            result = self._fanart
        elif info_id == 'icon':
            result = self._icon
        elif info_id == 'profile':
            result = common.CONFIG_PATH
        else:
            raise Exception(
                'Need to complete getAddonInfo mock for info_id: ' + info_id)

        if not CONFIG['disable_xbmcaddon_mock_log']:
            print('[FakeAddon] getAddonInfo of "' + info_id + '" --> "' + result + '"')
        return result

    def getSetting(self, setting_id):
        if not CONFIG['disable_xbmcaddon_mock_log']:
            print('[FakeAddon] getSetting of "' + setting_id + '" --> "' + self._settings.get(setting_id, '') + '"')
        return self._settings.get(setting_id, '')

    def setSetting(self, _id, value):
        if not CONFIG['disable_xbmcaddon_mock_log']:
            print('[FakeAddon] setSetting of "' + _id + '" --> "' + value + '"')
        self._settings[_id] = value

    def getLocalizedString(self, id_):
        if not CONFIG['disable_xbmcaddon_mock_log']:
            print('[FakeAddon] getLocalizedString of ' + str(id_) + ' --> "' + self._labels.get(id_, str(id_)) + '"')
        return self._labels.get(id_, str(id_))


mock_xbmcaddon = mock.MagicMock()

mock_xbmcaddon.Addon.side_effect = FakeAddon

# Say to Python that the xbmcaddon module is mock_xbmcaddon
sys.modules['xbmcaddon'] = mock_xbmcaddon
