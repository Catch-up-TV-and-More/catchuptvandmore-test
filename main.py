#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import mock
import variables
from mock_xbmcaddon import *
from mock_xbmc import *
from mock_xbmcplugin import *
from mock_xbmcgui import *


print 'Catch-up TV & More simulator'
print ''

# Mock Kodi Python API
sys.modules['xbmcaddon'] = mock_xbmcaddon
sys.modules['xbmc'] = mock_xbmc
sys.modules['xbmcplugin'] = mock_xbmcplugin
sys.modules['xbmcgui'] = mock_xbmcgui


# Add codequick module path
sys.path.append(variables.CODEQUICK_PATH)

# Add Catch-up TV & More module path
sys.path.append(variables.ADDON_PATH)


base_url = 'plugin://plugin.video.catchuptvandmore/'
process_handle = '1'
query_string = ''


while(True):
    # Simulate Kodi argv
    fake_args = [base_url, process_handle, query_string]

    with mock.patch('sys.argv', fake_args):
        import addon
        addon.main()

        print ''
        print '==> Current menu:'
        print ''

        cnt = -1
        for item in variables.CURRENT_MENU:
            cnt = cnt + 1
            print_formated_listitem(item['listitem'], item['is_folder'], cnt)
            print ''
            # print '[URL] ' + item['url']

        print ''
        print 'Enter -1 to exit simulator'
        print ''

        try:
            next_item = int(raw_input('Item to select? \n'))
            if int(next_item) == -1:
                break

            else:
                next_item_splited = variables.CURRENT_MENU[int(next_item)]['url'].split('?')
                base_url = next_item_splited[0]
                query_string = '?' + next_item_splited[1]
        except ValueError:
            pass

        # Clear previous menu
        variables.CURRENT_MENU = []


print ''
print 'Exit Catch-up TV & More simulator'
