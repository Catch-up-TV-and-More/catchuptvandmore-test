# Catch-up TV & More test script

## Introduction

The purpose of this script is multiple:

* Run the plugin outsite Kodi and navigate in the different menus
* Easily custimize the add-on settings
* Configure a preset menu selections
* Launch an in-depth exploration of all menu and sub-menus of the add-on *(soon)*


## How it works?

This module works without modifying the original Catch-up TV & More source code. Thereby you can develop the add-on and test it at the same time in Kodi and in your terminal with this test module.
The different Kodi modules (xbmc, xbmcgui, xbmcaddon and xbmcplugin) are "hooked" with the aid of the mock python module.

## How to do?

Just clone this repository, edit the `config.py` file according to your configuration and run the main file with the `python3 main.py` command.
Also, it can be useful to log the tester stdout in a text file with `tee`.

Finally, this is my command to run the script with the STOUD and STDERR redirection:

```bash
python3 main.py 2>&1| tee ./log.txt
```

## Configuration file

You need to customize the `config.py` file.

This is the variables list to set and a short description:

* **ADDON_PATH** :
    * The absolute path of the plugin folder (plugin.video.catchuptvandmore)
* **ENABLE_AUTO_SELECT** :
    * If set to False, the add-on starts at the root menu and for each menu you have to choose the next menu to explore (this is the default behavior when you run the add-on in Kodi).
    * If set True, you need to edit the **AUTO_SELECT** dictionary. The key corresponds to the menu level and the value to the item to select. (e.g. with `AUTOSELECT = {0: 2, 1: 12, 3: 5}` the script will automatically choose the item number 2 at the root menu and enter in it. Then it will select item number 12 at the next level. But at the level number 2 you will have to choose the item to select. Finally for the level number 3 the script will select the item number 5).
* **ENABLE_FAKE_KODI_LOG** :
    * The CodeQuick framework uses the `xbmc.log()`function to print the different events. By setting this variable to True you allowed all messages originally send to `xbmc.log()` to be send on your STDOUT.
* **ENABLE_MOCK_XBMCADDON_LOG** :
    * If set to True, the script send a message with different information to STDOUT each time a function of `xbmcaddon` is called. (e.g. `getSetting(id)`).
* **ENABLE_MOCK_XBMC_LOG** :
	* Like **ENABLE_MOCK_XBMCADDON_LOG** but for the `xbmc` module.
* **CONSOLE_SIZE** :
    * This settings set the general width of the printed listing fake menu (if your screen is small or if your console window is not too much wide).
* **FAKE_SETTINGS** :
	* This dictionary corresponds to the `settings.xml` file of the add-on. Maybe soon the script will be able to directly parse and use the "real" `settings.xml` of the add-on...
* **FAKE_LABELS** :
    * This dictionary corresponds to the `strings.po` file of the add-on. Maybe soon the script will be able to directly parse and use the "real" `strings.po` of the add-on. For now you can generate this dictionary with the `generate_labels_dict_from_strings.po.py` file like that: `python generate_labels_dict_from_strings.po.py path_of_string.po_file`.







