#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import mock
import importlib
import subprocess
import bridge


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

# When you enter in the addon for the first time there is no query

root_plugin_url = {
    'base_url': 'plugin://plugin.video.catchuptvandmore/',
    'process_handle': '1',
    'query_string': ''
}

runtime.LISTINGS_STACK.append(root_plugin_url)


# Here we enter in the infinite loop that simulate the navigation in the plugin
while(True):

    # We need to simulate sys.argv Kodi mechanism with mock.patch
    plugin_url = runtime.LISTINGS_STACK[-1]
    fake_args = [plugin_url['base_url'], plugin_url['process_handle'], plugin_url['query_string']]

    with mock.patch('sys.argv', fake_args):

        for k, v in sys.modules.items():
            if 'plugin.video.catchuptvandmore' in str(v):
                importlib.reload(v)

        importlib.reload(addon)
        addon.main()

        if runtime.VIDEO_URL_TO_PLAY:
            p = subprocess.Popen("mpv " + runtime.VIDEO_URL_TO_PLAY, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            (output, err) = p.communicate()
            retval = p.wait()
            runtime.VIDEO_URL_TO_PLAY = ""
            runtime.LISTINGS_STACK.pop()
            continue

        items = runtime.CURRENT_MENU['items']
        print_formated_listing(items)

        if bridge.LAST_MENU_TRIGGER_ERROR:
            print(WARNING + ' The last selection triggered an error (see log above) ' + WARNING)
            print('')
            bridge.LAST_MENU_TRIGGER_ERROR = False

        # Now we have to know the next item to epxlore

        next_item = -2
        if config.ENABLE_AUTO_SELECT and runtime.CURRENT_LEVEL in config.AUTO_SELECT:
            next_item = config.AUTO_SELECT[runtime.CURRENT_LEVEL]
        else:

            # We wait the user input
            try:
                next_item = int(input('Next item to select? \n'))
            except ValueError:
                pass
            print('')

        if next_item == -2:
            # Just reload the same menu
            pass
        elif next_item == -1:
            # The user want to exit the simulator, let's break the loop
            break

        elif next_item == 0:
            # We want to go back in the previous menu
            runtime.LISTINGS_STACK.pop()

        else:
            # The user want to select an item
            next_item_splited = items[next_item - 1]['url'].split('?')

            runtime.LISTINGS_STACK.append({
                'base_url': next_item_splited[0],
                'process_handle': '1',
                'query_string': '?' + next_item_splited[1]
            })

            runtime.CURRENT_LEVEL += 1



print('')
print('Exit Catch-up TV & More simulator')
print('')
