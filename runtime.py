# -*- coding: utf-8 -*-

"""
This var simulates the current
navigation in the addon
"""
CURRENT_PATH = []


"""
This dict keeps tracks on each encountered
errors during the add-on navigation
"""
ALL_REPORTED_ERROR = []


"""
This is the stack of items to explore
if we are in auto exploration mode.
Each element of this stack is a path to the item to explore
"""
ITEMS_TO_EXPLORE = []


"""
This list contains all items already explored
"""
ITEMS_ALREADY_EXPLORED = set()


"""
To says that we have to reah the entry point
before starting the auto exploration
(Only used in auto exploration mode)
"""
PATH_TO_REACH = True


def get_path_keys_list(path):
    keys_list = []
    for menu in path:
        keys_list.append(menu['key'])

    return keys_list
