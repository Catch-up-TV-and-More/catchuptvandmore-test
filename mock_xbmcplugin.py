#!/usr/bin/env python
# -*- coding: utf-8 -*-
import mock


def fake_add_directory_items(handle, items, totalItems=0):
    for item in items:
        #pass
        print repr(item)
    return True


def fake_end_of_directory(handle, succeeded=True, updateListing=False, cacheToDisc=True):
    pass


mock_xbmcplugin = mock.MagicMock()
mock_xbmcplugin.addDirectoryItems.side_effect = fake_add_directory_items
mock_xbmcplugin.endOfDirectory.side_effect = fake_end_of_directory
