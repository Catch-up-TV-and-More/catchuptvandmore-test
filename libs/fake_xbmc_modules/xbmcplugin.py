# -*- coding: utf-8 -*-

from directory import Directory, Item
from route import Route
from config import Config
from custom_logger import CustomLogger

log = CustomLogger(__name__)

if Config.get('disable_xbmcplugin_mock_log'):
    log.set_log_level('ERROR')


def setContent(handle, content):
    pass


def setPluginCategory(handle, category):
    pass


def addDirectoryItems(handle, items_qd, totalItems=0):
    log.debug('addDirectoryItems of {} items'.format(totalItems))
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


def endOfDirectory(handle, succeeded=True, updateListing=False, cacheToDisc=True):
    log.debug('endOfDirectory(succeeded={}, updateListing={}, cacheToDisc={})'.format(succeeded, updateListing, cacheToDisc))
    Directory.current_directory.succeeded = succeeded
    Directory.current_directory.update_listing = updateListing


def setResolvedUrl(handle, succeeded, listitem):
    log.debug('setResolvedUrl: {}'.format(listitem._path))
    directory = Directory()
    directory.path = Route.current_explored_route.path
    item = Item()
    item.url = listitem._path
    item.listitem = listitem
    item.is_folder = False
    directory.items[1] = item
    Directory.current_directory = directory


def addSortMethod(handle, sortMethod, label2Mask=""):
    pass


SORT_METHOD_ALBUM = 14
SORT_METHOD_ALBUM_IGNORE_THE = 15
SORT_METHOD_ARTIST = 11
SORT_METHOD_ARTIST_IGNORE_THE = 13
SORT_METHOD_BITRATE = 43
SORT_METHOD_CHANNEL = 41
SORT_METHOD_COUNTRY = 17
SORT_METHOD_DATE = 3
SORT_METHOD_DATEADDED = 21
SORT_METHOD_DATE_TAKEN = 44
SORT_METHOD_DRIVE_TYPE = 6
SORT_METHOD_DURATION = 8
SORT_METHOD_EPISODE = 24
SORT_METHOD_FILE = 5
SORT_METHOD_FULLPATH = 35
SORT_METHOD_GENRE = 16
SORT_METHOD_LABEL = 1
SORT_METHOD_LABEL_IGNORE_FOLDERS = 36
SORT_METHOD_LABEL_IGNORE_THE = 2
SORT_METHOD_LASTPLAYED = 37
SORT_METHOD_LISTENERS = 39
SORT_METHOD_MPAA_RATING = 31
SORT_METHOD_NONE = 0
SORT_METHOD_PLAYCOUNT = 38
SORT_METHOD_PLAYLIST_ORDER = 23
SORT_METHOD_PRODUCTIONCODE = 28
SORT_METHOD_PROGRAM_COUNT = 22
SORT_METHOD_SIZE = 4
SORT_METHOD_SONG_RATING = 29
SORT_METHOD_SONG_USER_RATING = 30
SORT_METHOD_STUDIO = 33
SORT_METHOD_STUDIO_IGNORE_THE = 34
SORT_METHOD_TITLE = 9
SORT_METHOD_TITLE_IGNORE_THE = 10
SORT_METHOD_TRACKNUM = 7
SORT_METHOD_UNSORTED = 40
SORT_METHOD_VIDEO_RATING = 19
SORT_METHOD_VIDEO_RUNTIME = 32
SORT_METHOD_VIDEO_SORT_TITLE = 26
SORT_METHOD_VIDEO_SORT_TITLE_IGNORE_THE = 27
SORT_METHOD_VIDEO_TITLE = 25
SORT_METHOD_VIDEO_USER_RATING = 20
SORT_METHOD_VIDEO_YEAR = 18
