#!/usr/bin/env python
# -*- coding: utf-8 -*-
import mock
import variables


def fake_add_directory_items(handle, items, totalItems=0):
    for item in items:
        current_item = {}
        current_item['url'] = item[0]
        current_item['listitem'] = item[1]
        current_item['is_folder'] = item[2]
        variables.CURRENT_MENU.append(current_item)
    return True


def fake_end_of_directory(handle, succeeded=True, updateListing=False, cacheToDisc=True):
    pass


mock_xbmcplugin = mock.MagicMock()
mock_xbmcplugin.addDirectoryItems.side_effect = fake_add_directory_items
mock_xbmcplugin.endOfDirectory.side_effect = fake_end_of_directory
