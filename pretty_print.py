# -*- coding: utf-8 -*-
import config


def print_formated_listitem(listitem, is_folder, cnt):
    formated_item = ''
    if is_folder:
        formated_item += "* "
    else:
        formated_item += "- "

    formated_item += listitem.getLabel()
    formated_item += ' [' + str(cnt) + ']'

    print(formated_item)

    if config.ONLY_PRINT_ITEM_LABEL:
        return

    if listitem._art:
        for art_item_k, art_item_v in listitem._art.items():
            print('    - [' + art_item_k + '] = ' + art_item_v)

    print('')
