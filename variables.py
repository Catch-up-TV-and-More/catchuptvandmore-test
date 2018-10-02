#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

KODI_URLS = {}
MENUS = {}
CURRENT_LEVEL = 0


# TO ADAPT
ENABLE_FAKE_KODI_LOG = False
ENABLE_MOCK_XBMCADDON_LOG = False

# TO ADAPT
ONLY_LIST_ITEM_LABEL = True

# TO ADAPT
# Pour passer directement plusieurs
# menu d'un seul coup sans avoir à le faire à la main
USE_AUTO_SELECT = False
AUTO_SELECT = {
    1: 2,  # Au niveau 1, choisir l'item numéro 2 (Replay TV)
    2: 1  # Au niveau 2, choisi l'item numéro 1 (France)
}

# TO ADAPT
ADDON_ID = "plugin.video.catchuptvandmore"


CWD_PATH = os.path.dirname(os.path.abspath(__file__))
CODEQUICK_PATH = os.path.join(CWD_PATH, 'script.module.codequick', 'lib')

# TO ADAPT
ADDON_PATH = os.path.join(CWD_PATH, '..', 'plugin.video.catchuptvandmore')

ADDON_FANART_PATHFILE = os.path.join(ADDON_PATH, 'fanart.jpg')
ADDON_ICON_PATHFILE = os.path.join(ADDON_PATH, 'icon.png')
CONFIG_PATH = os.path.join(CWD_PATH, 'fake_config')

# TO ADAPT
FAKE_SETTINGS = {
    # Main menu
    'live_tv': 'true',
    'live_tv.order': '1',
    'replay': 'true',
    "replay.order": '2',
    'websites': 'true',
    'websites.order': '3',

    # Replay menu
    'fr_replay': 'true',
    'fr_replay.order': '1',

    # Replay menu fr
    'tf1': 'true',
    'tf1.order': '1'
}

# TO ADAPT
FAKE_LABELS = {
    30000: 'Main menu',
    30001: 'Countries',
    30002: 'Quality and content',
    30003: 'Download',
    30004: 'Accounts',
    30005: 'Advanced settings',
    30006: 'Channels',
    30007: 'Websites',
    30010: 'Hide main menu categories',
    30011: 'Hide channels',
    30012: 'To configure YTDL go settings of script.module.youtube.dl',
    30013: 'Hide countries',
    30014: 'Hide websites',
    30030: 'Live TV',
    30031: 'Catch-up TV',
    30032: 'Websites',
    30050: 'France',
    30051: 'Switzerland',
    30052: 'United Kingdom',
    30053: 'International',
    30054: 'Belgium',
    30055: 'Japan',
    30056: 'Canada',
    30057: 'United States of America',
    30058: 'Poland',
    30059: 'Spain',
    30060: 'Tunisia',
    30080: 'French channels',
    30081: 'Belgian channels',
    30082: 'Japanese channels',
    30083: 'Switzerland channels',
    30084: 'United Kingdom channels',
    30085: 'International channels',
    30086: 'Canadian channels',
    30087: 'United States channels',
    30088: 'Polish channels',
    30089: 'Spanish channels',
    30090: 'Tunisia channels',
    30150: 'Video quality',
    30151: 'Video quality (BEST|DEFAULT|DIALOG)',
    30152: 'Contents',
    30153: 'Arte: Choose Channel',
    30154: 'France 24: Choose Channel',
    30155: 'Euronews: Choose Channel',
    30156: 'MTV: Choose Channel',
    30157: 'DW: Choose Channel',
    30158: 'France 3 Régions: Choose region',
    30159: 'La 1ère: Choose region',
    30160: 'Bein Sports: Choose Channel',
    30161: 'QVC: Choose Channel',
    30162: 'NHK World: Choose Country',
    30163: 'CGTN: Choose Channel',
    30164: 'Paramount Channel: Choose Channel',
    30165: 'Realmadrid TV: Choose Channel',
    30166: 'Yes TV: Choose region',
    30167: 'TVP 3: Choose region',
    30200: 'Folder to Download',
    30201: 'Quality of the video to download',
    30202: 'Download in background',
    30240: 'NRJ Login',
    30241: 'NRJ Password',
    30242: 'VRT NU Login',
    30243: 'VRT NU Password',
    30340: 'Enable VPN feature',
    30341: 'OpenVPN filepath',
    30342: 'Import OpenVPN configuration file',
    30343: 'Delete OpenVPN configuration file',
    30344: 'Additional arguments',
    30345: 'Run OpenVPN with superuser privileges (sudo)',
    30346: 'Ask for sudo password',
    30347: 'Connect VPN',
    30348: 'Choose a name for OpenVPN configuration',
    30349: 'This OpenVPN configuration name already exists. Overwrite?',
    30350: 'Import cancelled',
    30351: 'Import failed. You must specify a name for the OpenVPN configuration',
    30352: 'Select OpenVPN configuration to run',
    30353: 'Enter your sudo password',
    30354: 'Started VPN connection',
    30355: 'Stopped VPN connection',
    30356: 'An existing OpenVPN instance appears to be running.',
    30357: 'Disconnect it?',
    30358: 'An error has occurred whilst trying to connect OpenVPN',
    30359: 'Disconnect VPN',
    30360: 'Select OpenVPN configuration to delete',
    30361: 'Connect/Disconnect VPN',
    30370: 'Clear cache',
    30371: 'Cache cleared',
    30500: 'Move down',
    30501: 'Move up',
    30502: 'Hide',
    30503: 'Download',
    30600: 'Information',
    30601: 'To re-enable hidden items go to the plugin settings',
    30700: 'More videos...',
    30701: 'All videos',
    30702: 'DRM protected video',
    30703: 'Search',
    30704: 'Last videos',
    30705: 'From A to Z',
    30706: 'Ascending',
    30707: 'Descending',
    30708: 'More programs...',
    30709: 'Choose video quality',
    30710: 'Video stream no longer exists',
    30711: 'Authentication failed',
    30712: 'Video with an account needed',
    30713: 'Geo-blocked video',
    30714: 'Search videos',
    30715: 'Search programs',
    30716: 'Video stream is not available'
}


