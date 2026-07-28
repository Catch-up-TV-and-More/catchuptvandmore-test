# -*- coding: utf-8 -*-

# Python modules imports
import argparse
import json
import os
import random
from xml.etree import ElementTree as ET

import polib

CWD_PATH = os.path.dirname(os.path.abspath(__file__))


def parse_settings_xml(settings_xml_filepath):
    settings = {}
    xml = ET.parse(settings_xml_filepath)
    for child in xml.iter():
        if child.tag == "setting":
            if "id" in child.attrib:
                value = ""
                # print(child.attrib)
                if "type" in child.attrib and child.attrib["type"] == "folder":
                    value = "/tmp"
                if "default" in child.attrib:
                    value = child.attrib["default"]
                settings[child.attrib["id"]] = value
    return settings


def parse_accounts_settings_xml(settings_xml_filepath):
    settings = {}
    xml = ET.parse(settings_xml_filepath)
    for child in xml.iter():
        if child.tag == "setting":
            if "id" in child.attrib and ("login" in child.attrib["id"] or "password" in child.attrib["id"]):
                settings[child.attrib["id"]] = child.text
    return settings


def parse_strings_po(strings_po_filepath):
    labels = {}
    po = polib.pofile(strings_po_filepath)
    for entry in po:
        key = entry.msgctxt
        key = int(key.replace("#", ""))
        labels[key] = entry.msgid
    return labels


class ConfigMC(type):
    def __str__(cls):
        s = "* Configuration:"
        for k, v in cls._config.items():
            s += "\n\t- {}: {}".format(k, str(v))
        return s


class Config(metaclass=ConfigMC):
    """Singleton class to define user configuration"""

    _config = {}

    @classmethod
    def get(cls, item):
        return cls._config[item]

    @classmethod
    def init_config(cls):

        parser = argparse.ArgumentParser(description="Catch-up TV & More simulator")

        parser.add_argument(
            "-a",
            "--addon-path",
            default="",
            help="Path of plugin.video.catchuptvandmore",
        )
        parser.add_argument(
            "-p",
            "--pickle",
            default="",
            help="Pickle",
        )
        parser.add_argument(
            "-c",
            "--config-file",
            default="",
            help="Optional JSON config file (if given, CLI args are not taken !!)",
        )
        parser.add_argument(
            "-s",
            "--console-size",
            type=int,
            default=160,
            help="Your console size in order to compute the width of the fake Kodi menu [160]",
        )
        parser.add_argument(
            "--test-modules",
            action="store_true",
            help="Try to load each Python files to detect errors",
        )
        parser.add_argument(
            "--entry-point",
            default="1",
            help="Entry point of the simulation (separate items with dashes (e.g. '1-2-1-13')) [1]",
        )
        parser.add_argument(
            "--exit-after-x-errors",
            type=int,
            default=-1,
            help="Exit simulator after N errors encountered [-1]",
        )
        parser.add_argument(
            "--disable-video-player",
            action="store_true",
            help="Do not open mpv on video selection",
        )
        parser.add_argument(
            "--kodi-version",
            default="LEIA",
            choices=["LEIA", "KRYPTON", "JARVIS"],
            help="Kodi version to simulate [LEIA]",
        )
        parser.add_argument(
            "--print-all-explored-items",
            action="store_true",
            help="Print all explored items when exit the simulator",
        )
        parser.add_argument(
            "--disable-image-check", action="store_true", help="Do not check image URL"
        )
        parser.add_argument(
            "--autoreload-addon",
            action="store_true",
            help="Auto reload addon source files (usefull during dev)",
        )

        log_group = parser.add_argument_group("Logging")
        log_group.add_argument(
            "-l",
            "--log-level",
            default="info",
            choices=["debug", "info", "warning", "error", "critical"],
            help="Simulator log level",
        )
        log_group.add_argument(
            "--kodi-log-level",
            default="debug",
            choices=[
                "debug",
                "info",
                "notice",
                "warning",
                "error",
                "severe",
                "fatal",
                "none",
            ],
            help="Kodi log level",
        )
        log_group.add_argument(
            "--disable-xbmcaddon-mock-log",
            action="store_true",
            help="Disable log messages of xbmcaddon module functions calls",
        )
        log_group.add_argument(
            "--disable-xbmcplugin-mock-log",
            action="store_true",
            help="Disable log messages of xbmcplugin module functions calls",
        )
        log_group.add_argument(
            "--disable-xbmc-mock-log",
            action="store_true",
            help="Disable log messages of xbmc module functions calls",
        )

        auto_exploration_group = parser.add_argument_group("Auto exploration mode")
        auto_exploration_group.add_argument(
            "--auto-exploration",
            action="store_true",
            help="Enable auto exploration of addon menus",
        )
        auto_exploration_group.add_argument(
            "--max-items-per-menu",
            type=int,
            default=-1,
            help="Limit the number of items to explore per menu",
        )
        auto_exploration_group.add_argument(
            "--wait-time",
            type=float,
            default=1.0,
            help="Time to wait between each menu during exploration [1sec]",
        )
        auto_exploration_group.add_argument(
            "--max-items-to-explore",
            type=int,
            default=-1,
            help="Limit the total number of item to explore",
        )
        auto_exploration_group.add_argument(
            "--exploration-strategy",
            default="RANDOM",
            choices=["RANDOM", "FIRST", "LAST"],
            help="How to add items of explored menus to the stack to the stack of item to explore",
        )
        auto_exploration_group.add_argument(
            "--max-depth",
            type=int,
            default=-1,
            help="Set the max depth to explore from the entry point",
        )
        auto_exploration_group.add_argument(
            "--exclude-paths",
            default="",
            help="List of paths exclude from the exploration(e.g. '1-3, 1-2-1')",
        )
        auto_exploration_group.add_argument(
            "--skip-playable-items",
            action="store_true",
            help="Do not add playable items to the exploration stack",
        )
        auto_exploration_group.add_argument(
            "--timeout", type=int, default=-1, help="Auto exploration timeout [-1]"
        )

        cls._config = vars(parser.parse_args())

        config_json = {}

        # We have to check for a config file
        if cls._config["config_file"] != "":
            with open(cls._config["config_file"]) as f:
                config_json = json.load(f)

                # Check json dict
                for k in config_json.keys():
                    if k not in cls._config and k != "_comment":
                        raise Exception(
                            'The key "{}" in your json file is invalid'.format(k)
                        )
                    cls._config[k] = config_json[k]

        # We get the full path of the addon path
        if cls._config["addon_path"] == "":
            raise Exception(
                "You need to specify the path of plugin.video.catchuptvandmore (see --help)"
            )
        cls._config["addon_path"] = os.path.abspath(cls._config["addon_path"])

        cls._config["addon_id"] = "plugin.video.catchuptvandmore"
        cls._config["addon_fanart_filepath"] = os.path.join(
            cls._config["addon_path"], "fanart.jpg"
        )
        cls._config["addon_icon_filepath"] = os.path.join(
            cls._config["addon_path"], "icon.png"
        )
        cls._config["addon_en_strings_po_filepath"] = os.path.join(
            cls._config["addon_path"],
            "resources",
            "language",
            "resource.language.en_gb",
            "strings.po",
        )

        cls._config["codequick_path"] = os.path.join(
            CWD_PATH, "libs", "script.module.codequick", "lib"
        )
        cls._config["codequick_addon_path"] = os.path.join(
            CWD_PATH, "libs", "script.module.codequick"
        )
        cls._config["codequick_fanart_filepath"] = os.path.join(
            cls._config["codequick_addon_path"], "fanart.jpg"
        )
        cls._config["codequick_icon_filepath"] = os.path.join(
            cls._config["codequick_addon_path"], "icon.png"
        )
        cls._config["codequick_en_strings_po_filepath"] = os.path.join(
            cls._config["codequick_addon_path"],
            "resources",
            "language",
            "resource.language.en_gb",
            "strings.po",
        )

        cls._config["inputstreamhelper_path"] = os.path.join(
            CWD_PATH, "libs", "script.module.inputstreamhelper", "lib"
        )
        cls._config["inputstreamhelper_addon_path"] = os.path.join(
            CWD_PATH, "libs", "script.module.inputstreamhelper"
        )
        cls._config["inputstreamhelper_fanart_filepath"] = os.path.join(
            cls._config["inputstreamhelper_addon_path"], "fanart.jpg"
        )
        cls._config["inputstreamhelper_icon_filepath"] = os.path.join(
            cls._config["inputstreamhelper_addon_path"], "icon.png"
        )
        cls._config["inputstreamhelper_en_strings_po_filepath"] = os.path.join(
            cls._config["inputstreamhelper_addon_path"],
            "resources",
            "language",
            "resource.language.en_gb",
            "strings.po",
        )

        cls._config["youtubedl_path"] = os.path.join(
            CWD_PATH, "libs", "script.module.youtube.dl", "lib"
        )
        cls._config["youtubedl_addon_path"] = os.path.join(
            CWD_PATH, "libs", "script.module.youtube.dl"
        )
        cls._config["youtubedl_fanart_filepath"] = ""
        cls._config["youtubedl_icon_filepath"] = os.path.join(
            cls._config["youtubedl_addon_path"], "icon.png"
        )
        cls._config["youtubedl_en_strings_po_filepath"] = os.path.join(
            cls._config["youtubedl_addon_path"],
            "resources",
            "language",
            "resource.language.en_gb",
            "strings.po",
        )

        cls._config["kodi-six_path"] = os.path.join(
            CWD_PATH, "libs", "script.module.kodi-six", "libs"
        )
        cls._config["pyqrcode_path"] = os.path.join(
            CWD_PATH, "libs", "script.module.pyqrcode", "lib"
        )
        cls._config["tzlocal_path"] = os.path.join(
            CWD_PATH, "libs", "script.module.tzlocal", "lib"
        )

        cls._config["fake_xbmc_modules_path"] = os.path.join(
            CWD_PATH, "libs", "fake_xbmc_modules"
        )

        # Fake Kodi/userdata/addon_data/plugin.video.catchuptvandmore
        cls._config["userdata_path"] = os.path.join(CWD_PATH, "fake_userdata")

        # We convert the entry point to a list
        entry_point = []
        for item_key in cls._config["entry_point"].split("-"):
            entry_point.append(item_key)
        cls._config["entry_point"] = entry_point

        # We convert the exclude string to a list of list
        exclude_paths = []
        if cls._config["exclude_paths"] != "":
            exclude_paths_s = "".join(cls._config["exclude_paths"].split())
            for exclude in exclude_paths_s.split(","):
                exclude_path = []
                for item in exclude.split("-"):
                    exclude_path.append(int(item))
                exclude_paths.append(exclude_path)
        cls._config["exclude_paths"] = exclude_paths

        # We move max depth according to the entry point
        if cls._config["max_depth"] != -1:
            cls._config["max_depth"] = (
                cls._config["max_depth"] + len(cls._config["entry_point"]) - 1
            )

        # Parse settings.xml files
        addon_settings_filepath = os.path.join(
            Config.get("addon_path"), "resources", "settings.xml"
        )

        # Choose a random language
        cls._config["addon_settings"] = parse_settings_xml(addon_settings_filepath)
        cls._config["addon_settings"]["arte.language"] = random.choice(
            ["FR", "DE", "EN", "ES", "PL", "IT"]
        )
        cls._config["addon_settings"]["euronews.language"] = random.choice(
            ["FR", "EN", "AR", "DE", "IT", "ES", "PT", "RU", "TR", "FA", "GR", "HU"]
        )
        cls._config["addon_settings"]["france24.language"] = random.choice(
            ["FR", "EN", "AR", "ES"]
        )
        cls._config["addon_settings"]["mtv.language"] = random.choice(["FR"])
        cls._config["addon_settings"]["dw.language"] = random.choice(
            ["EN", "DE", "ES", "AR"]
        )
        cls._config["addon_settings"]["beinsports.language"] = random.choice(
            ["AU", "AR", "EN", "FR", "US", "ES", "NZ", "HK", "PH", "TH", "ID", "MY"]
        )
        cls._config["addon_settings"]["qvc.language"] = random.choice(
            ["JP", "DE", "IT", "UK", "US"]
        )
        cls._config["addon_settings"]["nhkworld.language"] = random.choice(
            ["Outside Japan", "In Japan"]
        )
        cls._config["addon_settings"]["cgtn.language"] = random.choice(
            ["FR", "EN", "AR", "ES", "RU"]
        )
        cls._config["addon_settings"]["paramountchannel.language"] = random.choice(
            ["ES", "IT"]
        )
        cls._config["addon_settings"]["rt.language"] = random.choice(
            ["FR", "EN", "AR", "ES"]
        )
        cls._config["addon_settings"]["tv5mondeplus.country"] = "BE"
        cls._config["addon_settings"]["tv5mondeplus.language"] = "fr"
        cls._config["addon_settings"]["france3regions.language"] = random.choice(
            [
                "Alpes",
                "Alsace",
                "Aquitaine",
                "Auvergne",
                "Bourgogne",
                "Bretagne",
                "Centre-Val de Loire",
                "Chapagne-Ardenne",
                "Corse",
                "Côte d'Azur",
                "Franche-Compté",
                "Languedoc-Roussillon",
                "Limousin",
                "Lorraine",
                "Midi-Pyrénées",
                "Nord-Pas-de-Calais",
                "Basse-Normandie",
                "Haute-Normandie",
                "Paris Île-de-France",
                "Pays de la Loire",
                "Picardie",
                "Poitou-Charentes",
                "Provence-Alpes",
                "Rhône-Alpes",
            ]
        )
        cls._config["addon_settings"]["la_1ere.language"] = random.choice(
            [
                "Guadeloupe",
                "Guyane",
                "Martinique",
                "Mayotte",
                "Nouvelle Calédonie",
                "Polynésie",
                "Réunion",
                "St-Pierre et Miquelon",
                "Wallis et Futuna",
                "Outre-mer",
            ]
        )
        cls._config["addon_settings"]["realmadridtv.language"] = random.choice(
            ["ES", "EN"]
        )
        cls._config["addon_settings"]["tvp3.language"] = random.choice(
            [
                "Białystok",
                "Bydgoszcz",
                "Gdańsk",
                "Gorzów Wielkopolski",
                "Katowice",
                "Kielce",
                "Kraków",
                "Lublin",
                "Łódź",
                "Olsztyn",
                "Opole",
                "Poznań",
                "Rzeszów",
                "Szczecin",
                "Warszawa",
                "Wrocław",
            ]
        )

        cls._config["addon_settings"]["tv_guide"] = "false"

        cls._config["codequick_fake_settings"] = {}

        inputstreamhelper_settings_filepath = os.path.join(
            Config.get("inputstreamhelper_addon_path"), "resources", "settings.xml"
        )
        cls._config["inputstreamhelper_fake_settings"] = parse_settings_xml(
            inputstreamhelper_settings_filepath
        )

        youtubedl_settings_filepath = os.path.join(
            Config.get("youtubedl_addon_path"), "resources", "settings.xml"
        )
        cls._config["youtubedl_fake_settings"] = parse_settings_xml(
            youtubedl_settings_filepath
        )

        # Parse english strings.po files
        cls._config["addon_labels"] = parse_strings_po(
            Config.get("addon_en_strings_po_filepath")
        )
        cls._config["codequick_labels"] = parse_strings_po(
            Config.get("codequick_en_strings_po_filepath")
        )
        cls._config["inputstreamhelper_labels"] = parse_strings_po(
            Config.get("inputstreamhelper_en_strings_po_filepath")
        )
        cls._config["youtubedl_labels"] = parse_strings_po(
            Config.get("youtubedl_en_strings_po_filepath")
        )
        cls._config["xbmc_labels"] = parse_strings_po(
            os.path.join(CWD_PATH, "libs", "fake_xbmc_modules", "strings.po")
        )

        cls.set_accounts()

        cls._config["addon_settings"]["stream_bitrate_limit"] = '0'
        cls._config["addon_settings"]["use_ia_hls_stream"] = "false"
        # cls._config["addon_settings"]["use_ia_hls_stream"] = "true"
        cls._config["addon_settings"]["use_ytdl_stream"] = "false"
        cls._config["addon_settings"]["quality"] = '1'

    @classmethod
    def set_accounts(cls):

        userdata_path = os.path.join(
            Config.get("addon_path"),
            "..",
            "..",
            "userdata",
            "addon_data",
            "plugin.video.catchuptvandmore",
            "settings.xml"
        )

        if not os.path.isfile(userdata_path):
            return

        user_accounts = parse_accounts_settings_xml(userdata_path)
        cls._config["addon_settings"].update(user_accounts)
