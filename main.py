#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

print('Catch-up TV & More tester')

# Add Codequick lib to python path
sys.path.append('./script.module.codequick/lib/')

# Add Kodistubs lib to python path
sys.path.append('./kodistubs/')

ADDON_PATH = '../plugin.video.catchuptvandmore'
sys.path.append(ADDON_PATH)

import addon
