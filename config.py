# -*- coding: utf-8 -*-
import os
import json
import argparse

parser = argparse.ArgumentParser(description='Catch-up TV & More simulator')

parser.add_argument('-a', '--addon-path', default='', help='Path of plugin.video.catchuptvandmore')
parser.add_argument('-c', '--config-file', default='', help='Optional JSON config file (CLI args take precedence over the config file)')
parser.add_argument('-s', '--console-size', type=int, default=160, help='Your console size in order to compute the width of the fake Kodi menu [160]')
parser.add_argument('--auto-select', default='', help='Auto select items from root menu, separate items with dashes (e.g. \'1-2-1-13\')')
parser.add_argument('--exit-on-error', action='store_true', help='Quit simulator at the first error encountered')
parser.add_argument('--disable-video-player', action='store_true', help='Do not open mpv on video slection')
parser.add_argument('--kodi-version', default='LEIA', choices=['LEIA', 'KRYPTON', 'JARVIS'], help='Kodi version to simulate [LEIA]')
parser.add_argument('--print-all-explored-items', action='store_true', help='Print all explored items when exit the simulator')


log_group = parser.add_argument_group('Logging')
log_group.add_argument('--disable-kodi-log', action='store_true', help='Disable stdout Kodi logging')
log_group.add_argument('--kodi-log-level', type=int, default=0, help='Minimum Kodi log level to be logging')
log_group.add_argument('--disable-xbmcaddon-mock-log', action='store_true', help='Disable log messages of xbmcaddon module functions calls')
log_group.add_argument('--disable-xbmc-mock-log', action='store_true', help='Disable log messages of xbmc module functions calls')


auto_exploration_group = parser.add_argument_group('Auto exploration mode')
auto_exploration_group.add_argument('--auto-exploration', action='store_true', help='Enable auto exploration of addon menus')
auto_exploration_group.add_argument('--entry-points', default='1', help='By default the auto exploration starts from the root menu but you can specify a list of entry points to explore (e.g. \'1, 1-2-1\')')
auto_exploration_group.add_argument('--max-items-per-menu', type=int, default=-1, help='Limit the number of items to explore per menu')
auto_exploration_group.add_argument('--wait-time', type=int, default=1, help='Time to wait between each menu during exploration [1sec]')
auto_exploration_group.add_argument('--max-items-to-explore', type=int, default=-1, help='Limit the total number of item to explore')


CONFIG_CLI = vars(parser.parse_args())


CONFIG_JSON = {}
# We have to check for a config file
if CONFIG_CLI['config_file'] != '':
    with open(CONFIG_CLI['config_file']) as f:
        CONFIG_JSON = json.load(f)

        # Check json dict
        for k in CONFIG_JSON.keys():
            if k not in CONFIG_CLI:
                raise Exception('The key "' + k + '" in your json file is invalid')


# We keep in priority the infos from the CLI
CONFIG = CONFIG_CLI
if 'addon_path' in CONFIG_JSON and CONFIG['addon_path'] == '':
    CONFIG['addon_path'] = CONFIG_JSON['addon_path']

if 'console_size' in CONFIG_JSON and CONFIG['console_size'] == 160:
    CONFIG['console_size'] = CONFIG_JSON['console_size']

if 'auto_select' in CONFIG_JSON and CONFIG['auto_select'] == '':
    CONFIG['auto_select'] = CONFIG_JSON['auto_select']

if 'auto_select' in CONFIG_JSON and CONFIG['auto_select'] == '':
    CONFIG['auto_select'] = CONFIG_JSON['auto_select']

if 'exit_on_error' in CONFIG_JSON and CONFIG['exit_on_error'] is False:
    CONFIG['exit_on_error'] = CONFIG_JSON['exit_on_error']

if 'disable_video_player' in CONFIG_JSON and CONFIG['disable_video_player'] is False:
    CONFIG['disable_video_player'] = CONFIG_JSON['disable_video_player']

if 'kodi_version' in CONFIG_JSON and CONFIG['kodi_version'] == 'LEIA':
    CONFIG['kodi_version'] = CONFIG_JSON['kodi_version']

if 'print_all_explored_items' in CONFIG_JSON and CONFIG['print_all_explored_items'] is False:
    CONFIG['print_all_explored_items'] = CONFIG_JSON['print_all_explored_items']

if 'disable_kodi_log' in CONFIG_JSON and CONFIG['disable_kodi_log'] is False:
    CONFIG['disable_kodi_log'] = CONFIG_JSON['disable_kodi_log']

if 'kodi_log_level' in CONFIG_JSON and CONFIG['kodi_log_level'] == 0:
    CONFIG['kodi_log_level'] = CONFIG_JSON['kodi_log_level']

if 'disable_xbmcaddon_mock_log' in CONFIG_JSON and CONFIG['disable_xbmcaddon_mock_log'] is False:
    CONFIG['disable_xbmcaddon_mock_log'] = CONFIG_JSON['disable_xbmcaddon_mock_log']

if 'disable_xbmc_mock_log' in CONFIG_JSON and CONFIG['disable_xbmc_mock_log'] is False:
    CONFIG['disable_xbmc_mock_log'] = CONFIG_JSON['disable_xbmc_mock_log']

if 'auto_exploration' in CONFIG_JSON and CONFIG['auto_exploration'] is False:
    CONFIG['auto_exploration'] = CONFIG_JSON['auto_exploration']

if 'entry_points' in CONFIG_JSON and CONFIG['entry_points'] == '1':
    CONFIG['entry_points'] = CONFIG_JSON['entry_points']

if 'max_items_per_menu' in CONFIG_JSON and CONFIG['max_items_per_menu'] == -1:
    CONFIG['max_items_per_menu'] = CONFIG_JSON['max_items_per_menu']

if 'wait_time' in CONFIG_JSON and CONFIG['wait_time'] == 1:
    CONFIG['wait_time'] = CONFIG_JSON['wait_time']

if 'max_items_to_explore' in CONFIG_JSON and CONFIG['max_items_to_explore'] == -1:
    CONFIG['max_items_to_explore'] = CONFIG_JSON['max_items_to_explore']


# We get the full path of the addon path
if CONFIG['addon_path'] == '':
    raise Exception('You need to specify the path of plugin.video.catchuptvandmore')
CONFIG['addon_path'] = os.path.abspath(CONFIG['addon_path'])


# We transform the auto select string to a list
if CONFIG['auto_select'] != '':
    auto_select_l = []
    for item in CONFIG['auto_select'].split('-'):
        auto_select_l.append(int(item))
    CONFIG['auto_select'] = auto_select_l


# We transform the entry points string to a list of list
entry_points_l = []
entry_points_s = "".join(CONFIG['entry_points'].split())
for ep in entry_points_s.split(','):
    entry_point_l = []
    for item in ep.split('-'):
        entry_point_l.append(int(item))
    entry_points_l.append(entry_point_l)
CONFIG['entry_points'] = entry_points_l


#################################################
#                                               #
#          Addon settings and labels            #
#                                               #
#################################################

"""
This dict simulate your settings.xml file
"""
ADDON_FAKE_SETTINGS = {
    # Main menu
    "live_tv": "true",
    "live_tv.order": "1",
    "replay": "true",
    "replay.order": "2",
    "websites": "true",
    "websites.order": "3",

    # Countries

    ## Live TV Countries
    "fr_live": "true",
    "fr_live.order": "1",
    "ch_live": "true",
    "ch_live.order": "2",
    "uk_live": "true",
    "uk_live.order": "3",
    "wo_live": "true",
    "wo_live.order": "4",
    "be_live": "true",
    "be_live.order": "5",
    "jp_live": "true",
    "jp_live.order": "6",
    "ca_live": "true",
    "ca_live.order": "7",
    "us_live": "true",
    "us_live.order": "8",
    "pl_live": "true",
    "pl_live.order": "9",
    "es_live": "true",
    "es_live.order": "10",

    ## Replay Countries
    "fr_replay": "true",
    "fr_replay.order": "1",
    "ch_replay": "true",
    "ch_replay.order": "2",
    "uk_replay": "true",
    "uk_replay.order": "3",
    "wo_replay": "true",
    "wo_replay.order": "4",
    "be_replay": "true",
    "be_replay.order": "5",
    "jp_replay": "true",
    "jp_replay.order": "6",
    "ca_replay": "true",
    "ca_replay.order": "7",
    "us_replay": "true",
    "us_replay.order": "8",
    "pl_replay": "true",
    "pl_replay.order": "9",
    "es_replay": "true",
    "es_replay.order": "10",

    # Channels

    ## Switzerland
    "rts": "true",
    "rts.order": "1",
    "rsi": "true",
    "rsi.order": "2",
    "srf": "true",
    "srf.order": "3",
    "rtr": "true",
    "rtr.order": "4",
    "swissinfo": "true",
    "swissinfo.order": "5",
    "rougetv": "true",
    "rougetv.order": "6",
    "tvm3": "true",
    "tvm3.order": "7",
    "becurioustv": "true",
    "becurioustv.order": "8",
    "rtsun": "true",
    "rtsun.order": "9",
    "rtsdeux": "true",
    "rtsdeux.order": "10",
    "rtsinfo": "true",
    "rtsinfo.order": "11",
    "rtscouleur3": "true",
    "rtscouleur3.order": "12",
    "rsila1": "true",
    "rsila1.order": "13",
    "rsila2": "true",
    "rsila2.order": "14",
    "srf1": "true",
    "srf1.order": "15",
    "srfinfo": "true",
    "srfinfo.order": "16",
    "srfzwei": "true",
    "srfzwei.order": "17",
    "rtraufsrf1": "true",
    "rtraufsrf1.order": "18",
    "rtraufsrfinfo": "true",
    "rtraufsrfinfo.order": "19",
    "rtraufsrf2": "true",
    "rtraufsrf2.order": "20",
    "teleticino": "true",
    "teleticino.order": "21",

    ## United Kingdom
    "blaze": "true",
    "blaze.order": "1",
    "dave": "true",
    "dave.order": "2",
    "really": "true",
    "really.order": "3",
    "yesterday": "true",
    "yesterday.order": "4",
    "drama": "true",
    "drama.order": "5",
    "skynews": "true",
    "skynews.order": "6",
    "skysports": "true",
    "skysports.order": "7",
    "stv": "true",
    "stv.order": "8",
    "questod": "true",
    "questod.order": "9",
    "hearttv": "true",
    "hearttv.order": "10",

    ## International
    "tv5mondeafrique": "true",
    "tv5mondeafrique.order": "1",
    "euronews": "true",
    "euronews.order": "2",
    "arte": "true",
    "arte.order": "3",
    "france24": "true",
    "france24.order": "4",
    "nhkworld": "true",
    "nhkworld.order": "5",
    "tv5monde": "true",
    "tv5monde.order": "6",
    "tivi5monde": "true",
    "tivi5monde.order": "7",
    "bvn": "true",
    "bvn.order": "8",
    "icitelevision": "true",
    "icitelevision.order": "9",
    "mtv": "true",
    "mtv.order": "10",
    "arirang": "true",
    "arirang.order": "11",
    "dw": "true",
    "dw.order": "12",
    "beinsports": "true",
    "beinsports.order": "13",
    "souvenirsfromearth": "true",
    "souvenirsfromearth.order": "14",
    "qvc": "true",
    "qvc.order": "15",
    "icirdi": "true",
    "icirdi.order": "16",
    "cgtn": "true",
    "cgtn.order": "17",
    "cgtndocumentary": "true",
    "cgtndocumentary.order": "18",
    "paramountchannel": "true",
    "paramountchannel.order": "19",
    "afriquemedia": "true",
    "afriquemedia.order": "20",
    "tv5mondefbs": "true",
    "tv5mondefbs.order": "21",
    "tv5mondeinfo": "true",
    "tv5mondeinfo.order": "22",
    "channelnewsasia": "true",
    "channelnewsasia.order": "23",

    ## Belgium
    "brf": "true",
    "brf.order": "1",
    "rtl_tvi": "true",
    "rtl_tvi.order": "2",
    "plug_rtl": "true",
    "plug_rtl.order": "3",
    "club_rtl": "true",
    "club_rtl.order": "4",
    "vrt": "true",
    "vrt.order": "5",
    "telemb": "true",
    "telemb.order": "6",
    "rtc": "true",
    "rtc.order": "7",
    "auvio": "true",
    "auvio.order": "8",
    "tvlux": "true",
    "tvlux.order": "9",
    "rtl_info": "true",
    "rtl_info.order": "10",
    "bel_rtl": "true",
    "bel_rtl.order": "11",
    "contact": "true",
    "contact.order": "12",
    "bx1": "true",
    "bx1.order": "13",
    "een": "true",
    "een.order": "14",
    "canvas": "true",
    "canvas.order": "15",
    "ketnet": "true",
    "ketnet.order": "16",
    "nrjhitstvbe": "true",
    "nrjhitstvbe.order": "17",
    "rtl_sport": "true",
    "rtl_sport.order": "18",

    ## France
    "tf1": "true",
    "tf1.order": "1",
    "france-2": "true",
    "france-2.order": "2",
    "france-3": "true",
    "france-3.order": "3",
    "canalplus": "true",
    "canalplus.order": "4",
    "france-5": "true",
    "france-5.order": "5",
    "m6": "true",
    "m6.order": "6",
    "c8": "true",
    "c8.order": "7",
    "w9": "true",
    "w9.order": "8",
    "tmc": "true",
    "tmc.order": "9",
    "tfx": "true",
    "tfx.order": "10",
    "nrj12": "true",
    "nrj12.order": "11",
    "france-4": "true",
    "france-4.order": "12",
    "bfmtv": "true",
    "bfmtv.order": "13",
    "cnews": "true",
    "cnews.order": "14",
    "cstar": "true",
    "cstar.order": "15",
    "gulli": "true",
    "gulli.order": "16",
    "france-o": "true",
    "france-o.order": "17",
    "tf1-series-films": "true",
    "tf1-series-films.order": "18",
    "lequipe": "true",
    "lequipe.order": "19",
    "6ter": "true",
    "6ter.order": "20",
    "rmcstory": "true",
    "rmcstory.order": "21",
    "cherie25": "true",
    "cherie25.order": "22",
    "la_1ere": "true",
    "la_1ere.order": "23",
    "franceinfo": "true",
    "franceinfo.order": "24",
    "bfmbusiness": "true",
    "bfmbusiness.order": "25",
    "rmc": "true",
    "rmc.order": "26",
    "01net": "true",
    "01net.order": "27",
    "tfou": "true",
    "tfou.order": "28",
    "xtra": "true",
    "xtra.order": "29",
    "lci": "true",
    "lci.order": "30",
    "lcp": "true",
    "lcp.order": "31",
    "rmcdecouverte": "true",
    "rmcdecouverte.order": "32",
    "stories": "true",
    "stories.order": "33",
    "comedy": "true",
    "comedy.order": "34",
    "publicsenat": "true",
    "publicsenat.order": "35",
    "france3regions": "true",
    "france3regions.order": "36",
    "francetvsport": "true",
    "francetvsport.order": "37",
    "histoire": "true",
    "histoire.order": "38",
    "tvbreizh": "true",
    "tvbreizh.order": "39",
    "ushuaiatv": "true",
    "ushuaiatv.order": "40",
    "studio-4": "true",
    "studio-4.order": "41",
    "irl": "true",
    "irl.order": "42",
    "seasons": "true",
    "seasons.order": "43",
    "comedie": "true",
    "comedie.order": "44",
    "les-chaines-planete": "true",
    "les-chaines-planete.order": "45",
    "golfplus": "true",
    "golfplus.order": "46",
    "cineplus": "true",
    "cineplus.order": "47",
    "infosportplus": "true",
    "infosportplus.order": "48",
    "gameone": "true",
    "gameone.order": "49",
    "francetveducation": "true",
    "francetveducation.order": "50",
    "gong": "true",
    "gong.order": "51",
    "bfmparis": "true",
    "bfmparis.order": "52",
    "onzeo": "true",
    "onzeo.order": "53",
    "fun_radio": "true",
    "fun_radio.order": "54",
    "melodytv": "true",
    "melodytv.order": "55",
    "slash": "true",
    "slash.order": "56",
    "polar-plus": "true",
    "polar-plus.order": "57",
    "virginradiotv": "true",
    "virginradiotv.order": "58",
    "culturebox": "true",
    "culturebox.order": "59",
    "kto": "true",
    "kto.order": "60",
    "antennereunion": "true",
    "antennereunion.order": "61",
    "viaoccitanie": "true",
    "viaoccitanie.order": "62",
    "ouatchtv": "true",
    "ouatchtv.order": "63",
    "canal10": "true",
    "canal10.order": "64",
    "rtl2": "true",
    "rtl2.order": "65",
    "lachainemeteo": "true",
    "lachainemeteo.order": "66",

    ## Japan
    "nhknews": "true",
    "nhknews.order": "1",
    "nhklifestyle": "true",
    "nhklifestyle.order": "2",
    "tbsnews": "true",
    "tbsnews.order": "3",
    "ntv": "true",
    "ntv.order": "4",
    "ex": "true",
    "ex.order": "5",
    "tbs": "true",
    "tbs.order": "6",
    "tx": "true",
    "tx.order": "7",
    "mbs": "true",
    "mbs.order": "8",
    "abc": "true",
    "abc.order": "9",
    "ytv": "true",
    "ytv.order": "10",
    "ntvnews24": "true",
    "ntvnews24.order": "11",
    "japanetshoppingdx": "true",
    "japanetshoppingdx.order": "12",
    "cx": "true",
    "cx.order": "8",

    ## Canada
    "tv5": "true",
    "tv5.order": "1",
    "unis": "true",
    "unis.order": "2",
    "yestv": "true",
    "yestv.order": "3",
    "telequebec": "true",
    "telequebec.order": "4",
    "tva": "true",
    "tva.order": "5",
    "icitele": "true",
    "icitele.order": "6",
    "ntvca": "true",
    "ntvca.order": "7",

    ## United States
    "cbsnews": "true",
    "cbsnews.order": "1",
    "tbd": "true",
    "tbd.order": "2",
    "nycmedia": "true",
    "nycmedia.order": "3",
    "abcnews": "true",
    "abcnews.order": "4",
    "pbskids": "true",
    "pbskids.order": "5",

    ## Poland
    "tvp": "true",
    "tvp.order": "1",
    "tvp3": "true",
    "tvp3.order": "2",
    "tvpinfo": "true",
    "tvpinfo.order": "3",
    "tvppolonia": "true",
    "tvppolonia.order": "4",

    ## Spain
    "telecinco": "true",
    "telecinco.order": "1",
    "cuatro": "true",
    "cuatro.order": "2",
    "fdf": "true",
    "fdf.order": "3",
    "boing": "true",
    "boing.order": "4",
    "energy": "true",
    "energy.order": "5",
    "divinity": "true",
    "divinity.order": "6",
    "bemad": "true",
    "bemad.order": "7",
    "realmadridtv": "true",
    "realmadridtv.order": "8",
    "antena3": "true",
    "antena3.order": "9",
    "lasexta": "true",
    "lasexta.order": "10",
    "neox": "true",
    "neox.order": "11",
    "nova": "true",
    "nova.order": "12",
    "mega": "true",
    "mega.order": "13",
    "atreseries": "true",
    "atreseries.order": "14",

    ## Tunisia
    "watania1": "true",
    "watania1.order": "1",
    "watania2": "true",
    "watania2.order": "2",

    # Websites
    "allocine": "true",
    "allocine.order": "1",
    "tetesaclaques": "true",
    "tetesaclaques.order": "2",
    "taratata": "true",
    "taratata.order": "3",
    "noob": "true",
    "noob.order": "4",
    "culturepub": "true",
    "culturepub.order": "5",
    "autoplus": "true",
    "autoplus.order": "6",
    "notrehistoirech": "true",
    "notrehistoirech.order": "7",
    "30millionsdamis": "true",
    "30millionsdamis.order": "8",
    "elle": "true",
    "elle.order": "9",
    "nytimes": "true",
    "nytimes.order": "10",
    "fosdem": "true",
    "fosdem.order": "11",
    "ina": "true",
    "ina.order": "12",
    "onf": "true",
    "onf.order": "13",
    "nfb": "true",
    "nfb.order": "14",

    # Quality and Content
    "quality": "BEST",

    ## Content
    "arte.language": "FR",
    "euronews.language": "FR",
    "france24.language": "FR",
    "mtv.language": "FR",
    "dw.language": "EN",
    "beinsports.language": "FR",
    "qvc.language": "FR",
    "nhkworld.country": "Outside Japan",
    "cgtn.language": "FR",
    "paramountchannel.language": "ES",

    "france3.region": "Alpes",
    "la_1ere.region": "Guadeloupe",

    "realmadridtv.language": "ES",

    "yestv.region": "Ontario",

    "tvp3.region": "Białystok",

    # Download
    "dl_folder": "/tmp",
    "dl_quality": "Highest available",
    "dl_background": "false",

    # Account
    "nrj.login": "toto",
    "nrj.password": "toto",

    "vrt.login": 'toto',
    "vrt.password": "toto",

    # VPN
    "vpn.hide": "true",
    "vpn.openvpnfilepath": "/usr/bin/openvpn",
    "vpn.args": "",
    "vpn.sudo": "false",
    "vpn.sudopsw": "false",
    "show_hidden_items_information": "true"
}


"""
You can generate this dict with this command :
python generate_labels_dict_from_strings.po your_strings.po
if you need to use french labels
"""
ADDON_FAKE_LABELS = {
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
    30716: 'Video stream is not available',
}


CODEQUICK_FAKE_SETTINGS = {

}


CODEQUICK_FAKE_LABELS = {
    33078: 'Next page'
}
