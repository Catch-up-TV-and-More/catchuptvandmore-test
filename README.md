# Catch-up TV & More test script

## Introduction

The purpose of this script is multiple:

* Run the plugin outsite Kodi and navigate in the different menus
* Easily custimize the add-on settings
* Configure a preset menu selections
* Launch an in-depth exploration of all menus and sub-menus of the add-on


## How it works?

This module works without modifying the original Catch-up TV & More addon source code.

Thereby you can develop the add-on and test it at the same time in Kodi and in your terminal with this test module.

The different Kodi modules (xbmc, xbmcgui, xbmcaddon and xbmcplugin) are "hooked" with the aid of the mock python module.


## How to do?

Just clone this repository, and run this command:
```bash
python3 main.py -a path/to/catchup/tv/and/more/addon
```

If you want you can use a JSON configuration file but the parameters from the CLI overwrite the JSON parameters.

Look at the `config_sample.json` file as an example to build yours.
For the complete list of parameters along with theirs types check the help message with `python3 main.py -h`.


Also, it can be useful to log the tester stdout in a text file with `tee` with this command to copy STDOUT and STDERR in the file `log.txt`:
```bash
python3 main.py -c path/to/config/file 2>&1| tee ./log.txt
```



## Configuration

The information below use the CLI format but you can easily find the corresponding variable name for the JSON file (e.g. `--max-items-per-menu` ==> `max_items_per_menu`).


### General parameters

* **-a/--addon-path STRING**:
    * The path of the plugin folder (plugin.video.catchuptvandmore)

* **-c/--config-file STRING**:
    * The optional JSON configuration file path (:warning: CLI parameters take precedence over the JSON configuration file)

* **-s/--console-size INT**:
    * Your console size in order to compute the width of the fake Kodi menu during the simulation. You have to find the correct value for your terminal window size in order to prevent one line of the array overlapping on the next line
    * Default value: 160

* **--auto-select STRING**:
    * It would be useful when you open the simulator to directly reach the channel on which you are currently working. To do that just specify this channel path with this parameter. Each element of the path is the item number of each level met from the root menu (root menu number = 1). (e.g. --auto-select 1-2-1-13)

* **--exit-on-error**:
    * Quit simulator at the first plugin error encountered instead of reload the previous Kodi menu

* **--disable-video-player**:
    * Do not open mpv on video slection

* **--kodi-version STRING (LEIA, KRYPTON or JARVIS)**:
    * Kodi version to simulate
    * Default value: LEIA

* **--print-all-explored-items**:
    * Print all explored items when exit the simulator

* **--disable-image-check**:
    * Do not check each image/fanart URL to speed up similation


### Logging

* **--disable-kodi-log**:
    * The CodeQuick framework uses the `xbmc.log()` function to print the different events. By setting this flag you prevent all messages originally send to `xbmc.log()` to be print on your STDOUT.

* **--kodi-log-level INT**:
    * Minimum Kodi log level to be logging. (Smaller the number is and more verbose the log of Kodi will be)
    * Default value: 0

* **--disable-xbmcaddon-mock-log**:
    * Each time a function of `xbmcaddon` is called. (e.g. `getSetting(id)`), the simulator print a message. With this flag you prevent this logging information.

* **--disable-xbmc-mock-log**:
  * Like **--disable-xbmcaddon-mock-log** but for the `xbmc` module.

* **--disable-xbmc-mock-log**:
  * Like **--disable-xbmcaddon-mock-log** but for the `xbmc` module.


### Auto exploration mode

* **--auto-exploration**:
  * Enable the auto exploration mode of the simulator

* **--entry-point STRING**:
  * By default the auto exploration starts from the root menu but you can specify one or more entry points of the addon to start the auto exploration (e.g. 1, 1-2-1, 1-3-4-1)

* **--max-items-per-menu INT**:
  * During the exploration, for each new menu explored, only add *max-items-per-menu* items to the paths to explore stack. If not set, add all the items of the menu

* **--wait-time FLOAT**:
    * Time to wait between each explored menu. To simulate an "human" usage...
    * Default value: 1 second

* **--max-items-to-explore INT**:
    * If the total number of item explored reach this value then stop the exploration

* **--exploration-strategy STRING**:
    * For each explored menu, this method says how to add items of the current menu in the stack of item to explore
        * FIRST: Add the "max-items-per-menu" first items of the menu
        * LAST: Add the "max-items-per-menu" last items of the menu
        * RANDOM (default): Add "max-items-per-menu" random items of the menu

* **--max-depth INT**:
    * To set the maximum allowed level to explore (usefull when there is a lot of "Next page")


### Addon settings and labels

* **ADDON_FAKE_SETTINGS** :
  * This dictionary corresponds to the `settings.xml` file of the add-on. Maybe soon the script will be able to directly parse and use the "real" `settings.xml` of the add-on...

* **ADDON_FAKE_LABELS** :
    * This dictionary corresponds to the `strings.po` file of the add-on. Maybe soon the script will be able to directly parse and use the "real" `strings.po` of the add-on. For now you can generate this dictionary with the `generate_labels_dict_from_strings.po.py` file like that: `python generate_labels_dict_from_strings.po.py path_of_string.po_file`.


## Cheat sheet of the fake Kodi menu

* General
   * :file_folder: : This item `is_folder`
   * :arrow_left: : Previous menu
   * :arrow_forward: This item `is_playable`

* Thumb and Fanart
   * :earth_africa: : The image come from the web (with an URL)
   * :desktop_computer: : The image come from the add-on resources
   * :white_check_mark: : The image URL is correct
   * :x: : There is something wrong and the image is not present or not valid (incorrect path for local image or wrong URL)
   * :tv: : This thumb or fanart is respectively the thumb or fanart of Catch-up TV & more (our official logo)



## Modules needed

* urlquick
* polib
* mock
* htmlement




