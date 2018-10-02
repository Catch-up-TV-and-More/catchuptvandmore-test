#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import mock
import variables
from mock_xbmcaddon import *
from mock_xbmc import *
from mock_xbmcplugin import *
from mock_xbmcgui import *


print ''
print '# Catch-up TV & More simulator'
print '## Enter -1 to exit simulator during addon navigation'

# Mock Kodi Python API
sys.modules['xbmcaddon'] = mock_xbmcaddon
sys.modules['xbmc'] = mock_xbmc
sys.modules['xbmcplugin'] = mock_xbmcplugin
sys.modules['xbmcgui'] = mock_xbmcgui


# Add codequick module path
sys.path.append(variables.CODEQUICK_PATH)

# Add Catch-up TV & More module path
sys.path.append(variables.ADDON_PATH)

variables.KODI_URLS[0] = {
    'base_url': 'plugin://plugin.video.catchuptvandmore/',
    'process_handle': '1',
    'query_string': ''
}


while(True):

    # Simulate Kodi argv
    kodi_url = variables.KODI_URLS[variables.CURRENT_LEVEL]
    fake_args = [kodi_url['base_url'], kodi_url['process_handle'], kodi_url['query_string']]

    with mock.patch('sys.argv', fake_args):
        import addon
        addon.main()

        print ''
        print '==> Current menu:'
        print ''

        cnt = 0
        if variables.CURRENT_LEVEL >= 1:
            print '* Previous menu [0]'

        for item in variables.MENUS[variables.CURRENT_LEVEL]:
            cnt = cnt + 1
            print_formated_listitem(item['listitem'], item['is_folder'], cnt)
            # print '[URL] ' + item['url']

        print ''
        try:
            next_item = 0
            if variables.USE_AUTO_SELECT and variables.CURRENT_LEVEL in variables.AUTO_SELECT:
                next_item = variables.AUTO_SELECT[variables.CURRENT_LEVEL]
            else:
                next_item = int(raw_input('Item to select? \n'))

            if next_item == -1:
                break

            elif next_item == 0:
                variables.CURRENT_LEVEL = variables.CURRENT_LEVEL - 1

            else:
                next_item_splited = variables.MENUS[variables.CURRENT_LEVEL][next_item - 1]['url'].split('?')

                variables.CURRENT_LEVEL = variables.CURRENT_LEVEL + 1

                variables.KODI_URLS[variables.CURRENT_LEVEL] = {
                    'base_url': next_item_splited[0],
                    'process_handle': '1',
                    'query_string': '?' + next_item_splited[1]
                }
        except ValueError:
            pass



print ''
print 'Exit Catch-up TV & More simulator'
