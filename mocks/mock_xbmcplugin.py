# -*- coding: utf-8 -*-

# The unicode_literals import only has
# an effect on Python 2.
# It makes string literals as unicode like in Python 3
from __future__ import unicode_literals


import sys
import mock

from directory import Directory, Item
from route import Route


def fake_add_directory_items(handle, items_qd, totalItems=0):
    directory = Directory()
    directory.path = Route.current_explored_route.path

    cnt = 0
    for item_cq in items_qd:
        item = Item()
        cnt += 1
        item.url = item_cq[0]
        item.listitem = item_cq[1]
        item.is_folder = item_cq[2]
        item.key = cnt

        directory.items[cnt] = item

    Directory.current_directory = directory
    return True


def fake_end_of_directory(handle, succeeded=True, updateListing=False, cacheToDisc=True):
    if updateListing:
        print('UPDATE LISTING TO IMPLEMENT')
        exit(-1)
    Directory.current_directory.succeeded = succeeded
    Directory.current_directory.update_listing = updateListing


def fake_set_resolve_url(handle, succeeded, listitem):
    directory = Directory()
    directory.path = Route.current_explored_route.path
    item = Item()
    item.url = listitem._path
    item.listitem = listitem
    item.is_folder = False
    directory.items[1] = item
    Directory.current_directory = directory


def fake_add_sort_method(handle, sortMethod, label2Mask=""):
    pass


mock_xbmcplugin = mock.MagicMock()

mock_xbmcplugin.addDirectoryItems.side_effect = fake_add_directory_items
mock_xbmcplugin.endOfDirectory.side_effect = fake_end_of_directory
mock_xbmcplugin.setResolvedUrl.side_effect = fake_set_resolve_url
mock_xbmcplugin.addSortMethod.side_effect = fake_add_sort_method


mock_xbmcplugin.SORT_METHOD_ALBUM = 14
mock_xbmcplugin.SORT_METHOD_ALBUM_IGNORE_THE = 15
mock_xbmcplugin.SORT_METHOD_ARTIST = 11
mock_xbmcplugin.SORT_METHOD_ARTIST_IGNORE_THE = 13
mock_xbmcplugin.SORT_METHOD_BITRATE = 43
mock_xbmcplugin.SORT_METHOD_CHANNEL = 41
mock_xbmcplugin.SORT_METHOD_COUNTRY = 17
mock_xbmcplugin.SORT_METHOD_DATE = 3
mock_xbmcplugin.SORT_METHOD_DATEADDED = 21
mock_xbmcplugin.SORT_METHOD_DATE_TAKEN = 44
mock_xbmcplugin.SORT_METHOD_DRIVE_TYPE = 6
mock_xbmcplugin.SORT_METHOD_DURATION = 8
mock_xbmcplugin.SORT_METHOD_EPISODE = 24
mock_xbmcplugin.SORT_METHOD_FILE = 5
mock_xbmcplugin.SORT_METHOD_FULLPATH = 35
mock_xbmcplugin.SORT_METHOD_GENRE = 16
mock_xbmcplugin.SORT_METHOD_LABEL = 1
mock_xbmcplugin.SORT_METHOD_LABEL_IGNORE_FOLDERS = 36
mock_xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE = 2
mock_xbmcplugin.SORT_METHOD_LASTPLAYED = 37
mock_xbmcplugin.SORT_METHOD_LISTENERS = 39
mock_xbmcplugin.SORT_METHOD_MPAA_RATING = 31
mock_xbmcplugin.SORT_METHOD_NONE = 0
mock_xbmcplugin.SORT_METHOD_PLAYCOUNT = 38
mock_xbmcplugin.SORT_METHOD_PLAYLIST_ORDER = 23
mock_xbmcplugin.SORT_METHOD_PRODUCTIONCODE = 28
mock_xbmcplugin.SORT_METHOD_PROGRAM_COUNT = 22
mock_xbmcplugin.SORT_METHOD_SIZE = 4
mock_xbmcplugin.SORT_METHOD_SONG_RATING = 29
mock_xbmcplugin.SORT_METHOD_SONG_USER_RATING = 30
mock_xbmcplugin.SORT_METHOD_STUDIO = 33
mock_xbmcplugin.SORT_METHOD_STUDIO_IGNORE_THE = 34
mock_xbmcplugin.SORT_METHOD_TITLE = 9
mock_xbmcplugin.SORT_METHOD_TITLE_IGNORE_THE = 10
mock_xbmcplugin.SORT_METHOD_TRACKNUM = 7
mock_xbmcplugin.SORT_METHOD_UNSORTED = 40
mock_xbmcplugin.SORT_METHOD_VIDEO_RATING = 19
mock_xbmcplugin.SORT_METHOD_VIDEO_RUNTIME = 32
mock_xbmcplugin.SORT_METHOD_VIDEO_SORT_TITLE = 26
mock_xbmcplugin.SORT_METHOD_VIDEO_SORT_TITLE_IGNORE_THE = 27
mock_xbmcplugin.SORT_METHOD_VIDEO_TITLE = 25
mock_xbmcplugin.SORT_METHOD_VIDEO_USER_RATING = 20
mock_xbmcplugin.SORT_METHOD_VIDEO_YEAR = 18

# Say to Python that the xbmcplugin module is mock_xbmcplugin
sys.modules['xbmcplugin'] = mock_xbmcplugin
