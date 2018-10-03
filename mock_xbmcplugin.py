# -*- coding: utf-8 -*-
import sys
import mock
import runtime


def fake_add_directory_items(handle, items, totalItems=0):
    runtime.CURRENT_MENU['items'] = []
    for item in items:
        current_item = {}
        current_item['url'] = item[0]
        current_item['listitem'] = item[1]
        current_item['is_folder'] = item[2]

        runtime.CURRENT_MENU['items'].append(current_item)
    return True


def fake_end_of_directory(handle, succeeded=True, updateListing=False, cacheToDisc=True):
    pass


def fake_set_resolve_url(handle, succeeded, listitem):
    if listitem._path:
        print('[path] = ' + listitem._path)
        runtime.VIDEO_URL_TO_PLAY = listitem._path


mock_xbmcplugin = mock.MagicMock()

mock_xbmcplugin.addDirectoryItems.side_effect = fake_add_directory_items
mock_xbmcplugin.endOfDirectory.side_effect = fake_end_of_directory
mock_xbmcplugin.setResolvedUrl.side_effect = fake_set_resolve_url

# Say to Python that the xbmcplugin module is mock_xbmcplugin
sys.modules['xbmcplugin'] = mock_xbmcplugin
