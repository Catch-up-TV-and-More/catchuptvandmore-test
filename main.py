#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Python modules imports
import sys
import mock
from importlib import reload
import time

# User modules imports
from config import Config
from route import Route
from directory import Directory
from runtime_error import RuntimeErrorCQ
from auto_exploration import AutoExploration

WARNING = u'\U000026A0'


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
    import mocks.mock_xbmcvfs
    # import mocks.mock_youtube_dl

    import addon

    entry_point_reached = False

    # Init Route to root
    root = Route(label='Root menu', path=[1])
    Route.add_route_to_explore(root)

    while(Route.continue_epxloration()):
        print('\n[DEBUG] Loop entry')

        current_route = Route.get_route_to_explore()

        # Check if the entry point was reached
        if current_route.path == Config.get('entry_point'):
            print('[DEBUG] Entry point ({}) reached'.format(Config.get('entry_point')))
            entry_point_reached = True

        # Hock sys.argv
        with mock.patch('sys.argv', current_route.get_fake_sys_argv()):

            if Config.get('autoreload_addon'):
                # We need to reload the addon module in order to be able
                # to modify the source code of the addon on the fly without restarting
                # the simulator
                # (usefull during dev)
                for k, v in sys.modules.items():
                    # print(str(k) + ' :: ' + str(v))
                    if 'plugin.video.catchuptvandmore' in str(v) and \
                            'plugin.video.catchuptvandmore/addon.py' not in str(v):
                        # print('\tRELOAD')
                        reload(v)
                reload(addon)

            # Simulate the addon execution
            addon.main()

            # We have to know the next item to epxlore
            # If next_item = -2 we just reload the addon we the same route
            next_item = -2

            # If an error was trigger
            if RuntimeErrorCQ.last_menu_triggered_error:
                print('\n' + WARNING + ' The last selection triggered an error (see log above) ' + WARNING + '\n')
                error = RuntimeErrorCQ(path=Route.pretty_exploring_routes())
                print(error)
                RuntimeErrorCQ.reset_error_trigger()

                if len(RuntimeErrorCQ.all_errors) >= Config.get('exit_after_x_errors'):
                    print('[DEBUG] Max number of error reached ({}) --> Exit'.format(Config.get('exit_after_x_errors')))
                    next_item = -1
                else:
                    print('[DEBUG] Max number of error not reached --> Go back')
                    next_item = 0

            # Else if succeeded is False (Happen when "No video found" notif is trigger)
            elif Directory.current_directory.succeeded is False:
                print('[DEBUG] endOfDirectory was called with succeeded=False --> Go back')
                next_item = 0


            # Else if the current directory is a playable item
            elif Directory.is_current_directory_playable():
                item = Directory.current_directory.items[1]
                print('PLAYABLE URL: {}'.format(item.url))
                next_item = 0


            # Else print the current directory
            else:
                print(Directory.current_directory)
                print(Route.pretty_exploring_routes() + '\n')


                # If the entry_point was not reached we follow the entry point path
                if not entry_point_reached:
                    next_item = Config.get('entry_point')[len(current_route.path)]
                    print('[DEBUG] Entry point not yet reached --> next item: {}'.format(next_item))


                # Else if we are in auto exploration
                elif Config.get('auto_exploration'):
                    print('[DEBUG] Auto exploration mode')
                    # If needed, add items of the current menu to explore later
                    AutoExploration.add_items_current_menu(current_route.path, Directory.current_directory)

                    # We wait a fake time
                    sys.stdout.flush()
                    time.sleep(Config.get('wait_time'))

                    # We ask for the next item to epxlore
                    next_item = AutoExploration.next_item_to_explore(current_route.path, Directory.current_directory)
                    print('[DEBUG] next_item selected by auto exploration: {}'.format(next_item))


                # Else we ask the user to choose the next item number
                else:
                    # We wait the user input
                    try:
                        sys.stdout.flush()
                        next_item = int(input('Next item to select? (-1 to exit, <enter> to reload same directory)\n'))
                        print('[DEBUG] choosen next_item: {}'.format(next_item))

                    except Exception:
                        pass
                    print('')


            # Else if the user wants to exit the simulator, let's break the loop
            if next_item == -1:
                break

            if Directory.current_directory is None:
                next_item = -2

            else:
                # If there is no item for this value, reload the same menu to prevent error
                if next_item > len(Directory.current_directory.items) or (next_item == 0 and len(current_route.path) <= 1):
                    next_item = -2


            # If next_item has the default value just reload the same menu
            if next_item == -2:
                pass

            # Else if the user want to go back in the previous menu
            elif next_item == 0:
                Route.previous_route()


            # Else if the user want an item
            else:
                selected_item = Directory.current_directory.items[next_item]
                Route.add_item_to_explore(selected_item)



    if Config.get('print_all_explored_items'):
        print('\n* All explored items:\n')
        for s in Route.explored_routes_l:
            print(s)

    ret_val = RuntimeErrorCQ.print_encountered_errors()
    return ret_val




if __name__ == '__main__':
    ret_val = main()
    sys.exit(ret_val)
