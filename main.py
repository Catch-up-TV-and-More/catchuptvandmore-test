#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Python modules imports
import sys
import mock
from importlib import reload


# User modules imports
from config import Config
from route import Route
from directory import Directory


def main():

    print('')
    print('#######################################')
    print('#                                     #')
    print('#     Catch-up TV & More simulator    #')
    print('#                                     #')
    print('#######################################')
    print('')

    # Get config
    Config.init_config()
    # print(Config)

    # Add codequick module to python path
    sys.path.append(Config.get('codequick_path'))

    # Add inputstreamhelper module to python path
    sys.path.append(Config.get('inputstreamhelper_path'))

    # Add Catch-up TV & More module to python path
    sys.path.append(Config.get('addon_path'))

    # import all hocked modules
    import mocks.mock_xbmcaddon
    import mocks.mock_xbmc
    import mocks.mock_xbmcplugin
    import mocks.mock_xbmcgui
    # import mocks.mock_xbmcvfs
    # import mocks.mock_youtube_dl

    import addon

    print('Entry point: ' + str(Config.get('entry_point')))

    entry_point_reached = False

    # Init Route to root
    root = Route(label='Root menu', path=[1])
    Route.add_route_to_explore(root)

    while(Route.continue_epxloration()):

        current_route = Route.get_route_to_explore()

        # Check if the entry point was reached
        if current_route.path == Config.get('entry_point'):
            entry_point_reached = True

        # Hock sys.argv
        with mock.patch('sys.argv', current_route.get_fake_sys_argv()):

            # Simulate the addon execution
            addon.main()

            # We have to know the next item to epxlore
            # If next_item = -2 we just reload the addon we the same route
            next_item = -2

            # Print the current directory
            print(Directory.current_directory)
            print(Route.print_exploring_routes())


            # If the entry_point was not reached we follow the entry point path
            if not entry_point_reached:
                next_item = Config.get('entry_point')[len(current_route.path)]

            # Else we ask the user to choose the next item number
            else:
                # We wait the user input
                try:
                    sys.stdout.flush()
                    next_item = int(input('Next item to select? (-1 to exit, <enter> to reload same directory)\n'))
                except Exception:
                    pass
                print('')


            # If there is no item for this value, reload the same menu to prevent error
            if next_item > len(Directory.current_directory.items) or (next_item == 0 and len(current_route.path) <= 1):
                next_item = -2


            # If next_item has the default value just reload the same menu
            if next_item == -2:
                pass

            # Else if the user wants to exit the simulator, let's break the loop
            elif next_item == -1:
                break

            # Else if the user want to go back in the previous menu
            elif next_item == 0:
                Route.previous_route()


            # Else if the user want an item
            else:
                selected_item = Directory.current_directory.items[next_item]
                Route.add_item_to_explore(selected_item)












if __name__ == '__main__':
    main()
