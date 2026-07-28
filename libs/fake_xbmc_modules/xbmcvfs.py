# -*- coding: utf-8 -*-
import os

CWD_PATH = os.path.dirname(os.path.abspath(__file__))


def exists(path: str) -> bool:
    return True


def translatePath(path):
    userdata_path = os.path.join(CWD_PATH, "..", "..", "fake_userdata", "headersCanal")
    path = path.replace("special://userdata/addon_data/plugin.video.catchuptvandmore/headersCanal", userdata_path)
    return path


class File(object):

    def __init__(self, *args, **kwargs):
        mod_args = args
        if type(args[0]) == str:
            l_args = list(args)
            l_args[0] = translatePath(l_args[0])
            mod_args = tuple(l_args)
        try:
            self.internal = open(*mod_args, **kwargs)
        except Exception as e:
            raise e

    def __getattr__(self, attr):
        return getattr(self.internal, attr)

    def __enter__(self):
        return self.internal

    def __exit__(self, type, value, traceback):
        pass
