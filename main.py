#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import mock
import variables
from mock_xbmcaddon import *
from mock_xbmc import *
from mock_xbmcplugin import *
from mock_xbmcgui import *


print 'Catch-up TV & More tester'
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

# Simulate Kodi argv
fake_args = ['plugin://plugin.video.catchuptvandmore/', '1', '']

with mock.patch('sys.argv', fake_args):
    import addon
    addon.main()


print ''
print 'Exit Catch-up TV & More tester'
