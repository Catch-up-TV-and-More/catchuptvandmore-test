# -*- coding: utf-8 -*-

"""
This var simulates the current "depth"
of your navigation in the addon

e.g. When you select the Addon from Kodi main menu you are coming at level 0
Then when you select Live TV you enter in level 1, etc
In the same way the current_level is decrementing when you do a "back"
"""
CURRENT_LEVEL = 0


"""
This list is used as a stack
This one keep tracks of each listings URLs in order
to simulate the "back" behavior
"""
LISTINGS_STACK = []


"""
This dict contains all relevant informations
concerning the current menu that Kodi is building
"""
CURRENT_MENU = {
    'items': []
}


VIDEO_URL_TO_PLAY = ""


"""
This dict keeps tracks on each encountered
errors during the add-on navigation
"""
ALL_REPORTED_ERROR = []