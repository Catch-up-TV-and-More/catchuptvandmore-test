# -*- coding: utf-8 -*-
import datetime


def print_msg(name, lvl, msg):
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("{} [{}] [{}] {}".format(time, lvl, name, msg))


class CustomLogger:

    global_log_level = 20

    levelno_dict = {
        'CRITICAL': 50,
        'ERROR': 40,
        'WARNING': 30,
        'INFO': 20,
        'DEBUG': 10
    }

    @classmethod
    def set_global_log_level(cls, log_level_s):
        cls.global_log_level = cls.levelno_dict.get(log_level_s, 20)

    def __init__(self, name):
        self.name = name
        self.log_level = CustomLogger.global_log_level

    def set_log_level(self, log_level_s):
        self.log_level = CustomLogger.levelno_dict.get(log_level_s, 20)

    def get_log_level(self):
        return self.log_level

    def debug(self, msg):
        if self.log_level <= 10:
            print_msg(self.name, 'debug', msg)

    def info(self, msg):
        if self.log_level <= 20:
            print_msg(self.name, 'info', msg)

    def warn(self, msg):
        if self.log_level <= 30:
            print_msg(self.name, 'warn', msg)

    def error(self, msg):
        if self.log_level <= 40:
            print_msg(self.name, 'error', msg)

    def critical(self, msg):
        if self.log_level <= 50:
            print_msg(self.name, 'critical', msg)
