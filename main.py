#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import mock
import importlib
import subprocess
import bridge
import time
import signal

import config
import common
import runtime
from pretty_print import *

import mock_xbmcaddon
import mock_xbmc
import mock_xbmcplugin
import mock_xbmcgui


print('')
print('#######################################')
print('#                                     #')
print('#     Catch-up TV & More simulator    #')
print('#                                     #')
print('#######################################')
print('')

print('# During addon navigation enter -1 to exit simulator')
print('')

# Add codequick module to python path
sys.path.append(common.CODEQUICK_PATH)

# Add Catch-up TV & More module to python path
sys.path.append(config.ADDON_PATH)

# And import Catch-up TV & More module
import addon

# When you enter in the addon for the first time there is no query and we are at root menu
root_menu_dict = {
    'key': 1,
    'label': 'Root menu',
    'base_url': 'plugin://plugin.video.catchuptvandmore/',
    'process_handle': '1',
    'query_string': ''
}

runtime.CURRENT_PATH.append(root_menu_dict)


# Here we enter in the infinite loop that simulate the navigation in the plugin
while(True):

    # We need to simulate sys.argv Kodi mechanism with mock.patch
    fake_args = [
        runtime.CURRENT_PATH[-1]['base_url'],
        runtime.CURRENT_PATH[-1]['process_handle'],
        runtime.CURRENT_PATH[-1]['query_string']
    ]

    with mock.patch('sys.argv', fake_args):

        # We need to reload the addon module in order to able
        # to modify the source code of the addon on the fly
        # (usefull during dev)
        for k, v in sys.modules.items():
            if 'plugin.video.catchuptvandmore' in str(v):
                importlib.reload(v)
        importlib.reload(addon)

        # Now we simulate the addon execution
        addon.main()

        # The current path as a list an as a tuple
        current_path_l = runtime.get_path_keys_list(runtime.CURRENT_PATH)
        current_path_t = tuple(current_path_l)

        # We have to know the next item to epxlore
        # If next_item = -2 we just reload the addon we the same sys.argv
        next_item = -2

        # If Kodi want to play a video we start mpv with the video
        if 'video' in runtime.CURRENT_PATH[-1]:
            # We need to go back to the last menu after the video player
            next_item = 0

            if not config.DISABLE_VIDEO_PLAYER:
                p = subprocess.Popen(['mpv', runtime.CURRENT_PATH[-1]['video']['url']], shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

                output = ''
                if config.DEPTH_EXPLORATION_MODE:
                    # We need to stop the video after some time
                    time.sleep(5)
                    p.send_signal(signal.SIGINT)

                    (output, err) = p.communicate()
                    retval = p.wait()  # Maybe not needed?

                else:
                    # The user need to manually close mpv
                    (output, err) = p.communicate()
                    retval = p.wait()

                MPV_STDOUT = output.decode('utf-8')
                # print('MPV_STDOUT: \n' + MPV_STDOUT)

                if 'Exiting... (Quit)' not in MPV_STDOUT:
                    print(WARNING + ' This video does not seem to work (see log above) ' + WARNING)
                    print('')

                    runtime.ALL_REPORTED_ERROR.append({
                        'type': 'Video',
                        'path': current_path_pp(runtime.CURRENT_PATH),
                        'route': bridge.TRIGGER_ERROR_ROUTE,
                        'params': bridge.TRIGGER_ERROR_PARAMS
                    })

                    if config.EXIT_IF_ERROR:
                        next_item = -1

        # We are in the basic menu case
        else:

            # If the last menu construction trigger an error
            # then Kodi just relaod the previous menu,
            # So we have to simulate the back function
            if bridge.LAST_MENU_TRIGGER_ERROR:
                print(WARNING + ' The last selection triggered an error (see log above) ' + WARNING)
                print('\tRoute that triggered the error: ' + bridge.TRIGGER_ERROR_ROUTE)
                print('\tParams that triggered the error: ' + bridge.TRIGGER_ERROR_PARAMS)
                print('')

                runtime.ALL_REPORTED_ERROR.append({
                    'type': 'Menu selection',
                    'path': current_path_pp(runtime.CURRENT_PATH),
                    'route': bridge.TRIGGER_ERROR_ROUTE,
                    'params': bridge.TRIGGER_ERROR_PARAMS
                })

                bridge.LAST_MENU_TRIGGER_ERROR = False
                bridge.TRIGGER_ERROR_ROUTE = ''
                bridge.TRIGGER_ERROR_PARAMS = ''

                next_item = 0

                if config.EXIT_IF_ERROR:
                    next_item = -1

            else:
                # We can print the menu
                items = runtime.CURRENT_PATH[-1]['menu']['items']
                print_formated_listing(items)
                print(current_path_pp(runtime.CURRENT_PATH))
                print('')

        # Now if next_item is still equal to -2 we have
        # to know what to do
        if next_item == -2:

            # If we are in auto exploration mode
            if config.DEPTH_EXPLORATION_MODE:

                # First we wait a fake time
                sys.stdout.flush()
                time.sleep(config.SLEEP_TIME)

                add_items_of_the_current_menu = True

                # If we already seen this menu
                if current_path_t in runtime.ITEMS_ALREADY_EXPLORED:
                    add_items_of_the_current_menu = False

                if runtime.PATH_TO_REACH:
                    # Else we have to start a new exploration from an entry point
                    entry_point = config.ENTRY_POINTS_TO_EXPLORE[-1]
                    print('We have to start exploration at the new entry point: ' + str(entry_point))

                    if len(current_path_l) > len(entry_point):
                        # We need to go back in previous level
                        add_items_of_the_current_menu = False
                        next_item = 0

                    elif len(current_path_l) < len(entry_point):
                        # We need to choose the right item
                        next_item = entry_point[len(current_path_l)]
                        add_items_of_the_current_menu = False

                    elif current_path_l == entry_point:
                        print('We just reach the entry point, we can start auto exploration')
                        config.ENTRY_POINTS_TO_EXPLORE.pop()
                        runtime.PATH_TO_REACH = False
                    else:
                        print('On ne devrait pas etre là ...')
                        exit(-1)

                if add_items_of_the_current_menu:

                    cnt = 0
                    for i in reversed(range(len(items))):
                        item = items[i]

                        new_path_l = list(current_path_l)
                        new_path_l.append(i + 1)
                        new_path_t = tuple(new_path_l)

                        if new_path_t not in runtime.ITEMS_ALREADY_EXPLORED:
                            runtime.ITEMS_TO_EXPLORE.append(new_path_l)
                            cnt += 1

                        if cnt >= config.MAX_ITEMS_NUMBER_PER_MENU:
                            break

                if next_item == -2:
                    if not runtime.ITEMS_TO_EXPLORE and not runtime.PATH_TO_REACH:
                        # If there is no more EP to explore
                        if not config.ENTRY_POINTS_TO_EXPLORE:
                            print('No more entry point to explore')
                            add_items_of_the_current_menu = False
                            next_item = -1
                        else:
                            runtime.PATH_TO_REACH = True

                    else:

                        item_to_explore = runtime.ITEMS_TO_EXPLORE[-1]
                        if len(current_path_l) > len(item_to_explore) or \
                                (len(current_path_l) == len(item_to_explore) and \
                                    current_path_l != item_to_explore):
                            next_item = 0
                        else:
                            runtime.ITEMS_TO_EXPLORE.pop()
                            next_item = item_to_explore[-1]

            # Else if we are not in auto exploration mode
            # and if the current level is in the AUTO_SELECT dict, then the script
            # auto select the item number of the dict
            elif len(runtime.CURRENT_PATH) in config.AUTO_SELECT and \
                    config.AUTO_SELECT[len(runtime.CURRENT_PATH)] != -1:
                next_item = config.AUTO_SELECT[len(runtime.CURRENT_PATH)]

            # Finaly, we ask the user to choose the item number
            else:
                # We wait the user input
                try:
                    sys.stdout.flush()
                    next_item = int(input('Next item to select? \n'))
                except ValueError:
                    pass
                print('')

        # We say that this path is now explored
        runtime.ITEMS_ALREADY_EXPLORED.add(current_path_t)

        # If next_item has the default value
        if next_item == -2:
            # Just reload the same menu
            pass

        # Else if the user wants to exit the simulator, let's break the loop
        elif next_item == -1:
            break

        # Else if the user want to go back in the previous menu
        elif next_item == 0:
            runtime.CURRENT_PATH.pop()

        # Else if the user selectes an item
        else:
            splitted_url = items[next_item - 1]['url'].split('?')
            next_menu_dict = {
                'key': next_item,
                'label': items[next_item - 1]['listitem'].getLabel(),
                'base_url': splitted_url[0],
                'process_handle': '1',
                'query_string': '?' + splitted_url[1]
            }

            runtime.CURRENT_PATH.append(next_menu_dict)


# We want to print all encountered errors
print_encountered_errors()

print('')
print('Exit Catch-up TV & More simulator')
print('')
