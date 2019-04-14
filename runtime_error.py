# -*- coding: utf-8 -*-

from colorama import Fore

WARNING = u'\U000026A0'



class RuntimeErrorCQ:

    last_menu_triggered_error = False
    last_error_message = ''
    last_codequick_route = ''
    last_codequick_callback_params = ''

    all_errors = []

    @classmethod
    def reset_error_trigger(cls):
        cls.last_menu_triggered_error = False
        cls.last_error_message = ''
        cls.last_codequick_route = ''
        cls.last_codequick_callback_params = ''

    @classmethod
    def print_encountered_errors(cls):
        if len(cls.all_errors) == 0:
            print('\n* No error encounteredn')
            return 0
        print('\n* Encountered errors list:\n')
        cnt = 0
        for error in cls.all_errors:
            print('\t- Error %s' % cnt)
            print(error)
            cnt += 1
        return 1


    def __init__(self, path):
        self.route = RuntimeErrorCQ.last_codequick_route
        self.params = dict(RuntimeErrorCQ.last_codequick_callback_params)
        self.msg = RuntimeErrorCQ.last_error_message
        self.pp_path = str(path)
        RuntimeErrorCQ.all_errors.append(self)

    def __str__(self):
        s = ''
        s += '* Path: {}'.format(self.pp_path) + '\n'
        s += '* Route: {}'.format(self.route) + '\n'
        s += '* Params: {}'.format(self.params) + '\n'
        s += '* Message: {}'.format(self.msg) + '\n'
        return s


