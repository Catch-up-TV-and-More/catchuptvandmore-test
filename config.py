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
parser.add_argument('--disable-image-check', action='store_true', help='Do not check image URL')


log_group = parser.add_argument_group('Logging')
log_group.add_argument('--disable-kodi-log', action='store_true', help='Disable stdout Kodi logging')
log_group.add_argument('--kodi-log-level', type=int, default=0, help='Minimum Kodi log level to be logging')
log_group.add_argument('--disable-xbmcaddon-mock-log', action='store_true', help='Disable log messages of xbmcaddon module functions calls')
log_group.add_argument('--disable-xbmc-mock-log', action='store_true', help='Disable log messages of xbmc module functions calls')


auto_exploration_group = parser.add_argument_group('Auto exploration mode')
auto_exploration_group.add_argument('--auto-exploration', action='store_true', help='Enable auto exploration of addon menus')
auto_exploration_group.add_argument('--entry-points', default='1', help='By default the auto exploration starts from the root menu but you can specify a list of entry points to explore (e.g. \'1, 1-2-1\')')
auto_exploration_group.add_argument('--max-items-per-menu', type=int, default=-1, help='Limit the number of items to explore per menu')
auto_exploration_group.add_argument('--wait-time', type=float, default=1.0, help='Time to wait between each menu during exploration [1sec]')
auto_exploration_group.add_argument('--max-items-to-explore', type=int, default=-1, help='Limit the total number of item to explore')
auto_exploration_group.add_argument('--exploration-strategy', default='RANDOM', choices=['RANDOM', 'FIRST', 'LAST'], help='How to add items of explored menus to the stack to the stack of item to explore')
auto_exploration_group.add_argument('--max-depth', type=int, default=-1, help='Set the max depth to explore')



CONFIG_CLI = vars(parser.parse_args())


CONFIG_JSON = {}
# We have to check for a config file
if CONFIG_CLI['config_file'] != '':
    with open(CONFIG_CLI['config_file']) as f:
        CONFIG_JSON = json.load(f)

        # Check json dict
        for k in CONFIG_JSON.keys():
            if k not in CONFIG_CLI and k != '_comment':
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

if 'disable_image_check' in CONFIG_JSON and CONFIG['disable_image_check'] is False:
    CONFIG['disable_image_check'] = CONFIG_JSON['disable_image_check']

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

if 'exploration_strategy' in CONFIG_JSON and CONFIG['exploration_strategy'] == 'RANDOM':
    CONFIG['exploration_strategy'] = CONFIG_JSON['exploration_strategy']

if 'max_depth' in CONFIG_JSON and CONFIG['max_depth'] == -1:
    CONFIG['max_depth'] = CONFIG_JSON['max_depth']


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


CODEQUICK_FAKE_SETTINGS = {

}


CODEQUICK_FAKE_LABELS = {
    33078: 'Next page'
}

INPUTSTREAMHELPER_FAKE_SETTINGS = {

}

INPUTSTREAMHELPER_FAKE_LABELS = {

}
