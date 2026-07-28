#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import glob
# Python modules imports
import os
import re
import sys
import time
from importlib import import_module, reload
from random import randint

import mock
from auto_exploration import AutoExploration
from config import Config
# User modules imports
from custom_logger import CustomLogger
from directory import Directory
from player import Player
from route import Route
from runtime_error import RuntimeErrorCQ

WARNING = u"\U000026A0"


def customize_sys_path():

    # Add fake xbmc modules (xbmc.py, xbmcgui.py, ...)
    sys.path.insert(1, Config.get("fake_xbmc_modules_path"))

    # Add kodi-six module to python path
    sys.path.insert(1, Config.get("kodi-six_path"))

    # Add pyqrcode module to python path
    sys.path.insert(1, Config.get("pyqrcode_path"))

    # Add tzlocal module to python path
    sys.path.insert(1, Config.get("tzlocal_path"))

    # Add codequick module to python path
    sys.path.append(Config.get("codequick_path"))

    # Add inputstreamhelper module to python path
    sys.path.append(Config.get("inputstreamhelper_path"))

    # Add Catch-up TV & More module to python path
    sys.path.insert(1, Config.get("addon_path"))

    # print(sys.path)


def test_modules(log):
    log.info("Try to load each Python files of the addons to detect errors")
    modules_to_test = []
    addon_full_path = os.path.dirname(os.path.abspath(Config.get("addon_path")))
    for root, dirs, files in os.walk(Config.get("addon_path")):
        for file in files:
            if file.endswith(".py"):
                module = os.path.join(root, file)
                module = module.replace(addon_full_path, "")
                module = module.replace(".py", "")
                module = module.replace("/plugin.video.catchuptvandmore/", "")
                module = module.replace("/", ".")
                if "tools" in module:
                    pass
                elif "__init__" in module:
                    pass
                elif "not_to_push" in module:
                    pass
                else:
                    modules_to_test.append(module)
    for module in modules_to_test:
        log.info("Try to load module '" + module + "'")
        try:
            import_module(module)
        except Exception as e:
            log.error("Failed to load module '" + module + "'")
            log.error("Error: {}".format(e))
            return -1
    return 0


def exploration_loop(log):
    import addon

    start_time = time.time()
    entry_point_reached = False

    if Config.get("pickle"):
        try:
            config_pickle = Config.get("pickle")
            query_string = re.sub(r'.*\?', '', config_pickle)
            base_url = config_pickle
            # base_url = re.sub(r'plugin://plugin.video.catchuptvandmore/', '', base_url)
            base_url = re.sub(r'\?.*', '', base_url)
            root = Route(label="pickle", query_string=query_string, path=[1], base_url=base_url)
            Route.add_route_to_explore(root)
        except Exception:
            pass
    else:
        # Init Route to root
        root = Route(label="Root menu", path=[1])
        Route.add_route_to_explore(root)

    while Route.continue_epxloration():
        log.debug("Loop entry")

        current_route = Route.get_route_to_explore()

        # Check if the entry point was reached
        if (
            len(current_route.path) == len(Config.get("entry_point"))
            and not entry_point_reached
        ):
            log.debug("Entry point ({}) reached".format(Config.get("entry_point")))
            entry_point_reached = True

        # Hock sys.argv
        with mock.patch("sys.argv", current_route.get_fake_sys_argv()):

            if Config.get("autoreload_addon"):
                # We need to reload the addon module in order to be able
                # to modify the source code of the addon on the fly without restarting
                # the simulator
                # (usefull during dev)
                for k, v in sys.modules.items():
                    # print(str(k) + ' :: ' + str(v))
                    if "plugin.video.catchuptvandmore" in str(
                        v
                    ) and "plugin.video.catchuptvandmore/addon.py" not in str(v):
                        # print('\tRELOAD')
                        reload(v)
                reload(addon)

            # We need to clean this var
            RuntimeErrorCQ.last_error_message = ""

            # Simulate the addon execution
            addon.main()

            # We have to know the next item to epxlore
            # If next_item = -2 we just reload the addon we the same route
            next_item = -2

            # If an error was trigger
            if RuntimeErrorCQ.last_menu_triggered_error:

                log.warn("")
                log.warn(
                    WARNING
                    + " The last selection triggered an error (see log above) "
                    + WARNING
                )
                log.warn("")

                error = RuntimeErrorCQ(path=Route.pretty_exploring_routes())
                print(error)
                RuntimeErrorCQ.reset_error_trigger()

                if len(RuntimeErrorCQ.all_errors) >= Config.get("exit_after_x_errors"):
                    log.info(
                        "Max number of error reached ({}) --> Exit".format(
                            Config.get("exit_after_x_errors")
                        )
                    )
                    next_item = -1
                else:
                    log.info("[DEBUG] Max number of error not reached --> Go back")
                    next_item = 0

            # Else if the current directory is a playable item
            elif Directory.is_current_directory_playable():
                item = Directory.current_directory.items[1]
                log.info("Playable URL of {}: {}".format(current_route.label, item.url))
                next_item = 0
                if not Config.get("disable_video_player"):
                    player = Player(item.url)
                    player.play()

            # Else if succeeded is False (Happen when "No video found" notif is trigger)
            elif Directory.current_directory.succeeded is False:
                log.info("endOfDirectory was called with succeeded=False --> Go back")
                next_item = 0

            # Else print the current directory
            else:
                print(Directory.current_directory)
                print(Route.pretty_exploring_routes() + "\n")

                # If the entry_point was not reached we follow the entry point path
                if not entry_point_reached:
                    next_item = Config.get("entry_point")[len(current_route.path)]
                    if next_item == "R":
                        next_item = randint(1, len(Directory.current_directory.items))
                        log.info(
                            "Entry point not yet reached --> random next item: {}".format(
                                next_item
                            )
                        )
                    else:
                        next_item = int(next_item)
                        log.info(
                            "Entry point not yet reached --> next item: {}".format(
                                next_item
                            )
                        )

                # Else if we are in auto exploration
                elif Config.get("auto_exploration"):
                    log.debug("Auto exploration mode")
                    # If needed, add items of the current menu to explore later
                    AutoExploration.add_items_current_menu(
                        current_route.path, Directory.current_directory
                    )

                    # We wait a fake time
                    sys.stdout.flush()
                    time.sleep(Config.get("wait_time"))

                    # We ask for the next item to epxlore
                    next_item = AutoExploration.next_item_to_explore(
                        current_route.path, Directory.current_directory
                    )
                    log.info(
                        "next_item selected by auto exploration: {}".format(next_item)
                    )

                # Else we ask the user to choose the next item number
                else:
                    # We wait the user input
                    try:
                        sys.stdout.flush()
                        next_item = int(
                            input(
                                "Next item to select? (-1 to exit, <enter> to reload same directory)\n"
                            )
                        )
                        log.info("Choosen next_item: {}".format(next_item))

                    except Exception:
                        pass
                    print("")

            # Check for timeout
            delta_time = time.time() - start_time
            if Config.get("timeout") != -1 and delta_time >= Config.get("timeout"):
                log.warn("AUTO EXPLORATION TIMEOUT --> Exit exploration")
                next_item = -1

            # Else if the user wants to exit the simulator, let's break the loop
            if next_item == -1:
                break

            if Directory.current_directory is None:
                next_item = -2

            else:
                # If there is no item for this value, reload the same menu to prevent error
                if next_item > len(Directory.current_directory.items) or (
                    next_item == 0 and len(current_route.path) <= 1
                ):
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


def main():

    # Get config
    Config.init_config()

    # Init custom logger
    CustomLogger.set_global_log_level(Config.get("log_level"))
    log = CustomLogger(__name__)

    log.info("")
    log.info("#######################################")
    log.info("#                                     #")
    log.info("#     Catch-up TV & More simulator    #")
    log.info("#                                     #")
    log.info("#######################################")
    log.info("")

    # Custumize sys.path to use custom modules
    customize_sys_path()

    if Config.get("test_modules"):
        return test_modules(log)
    else:
        exploration_loop(log)

        if Config.get("print_all_explored_items"):
            print("\n* All explored items:\n")
            for s in Route.explored_routes_l:
                print(s)

        RuntimeErrorCQ.print_encountered_warnings()
        ret_val = RuntimeErrorCQ.print_encountered_errors()
        return ret_val


if __name__ == "__main__":
    ret_val = main()
    sys.exit(ret_val)
