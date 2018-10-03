# -*- coding: utf-8 -*-
import config


def print_formated_listitem(listitem, is_folder, cnt, url):

    """
    Use '*' for folder item and '-' for playable item
    """
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

    if listitem._label2:
        print('    - [label2] = ' + listitem._label2)

    if listitem._path:
        print('    - [path] = ' + listitem._path)

    if listitem._art:
        for art_item_k, art_item_v in listitem._art.items():
            print('    - [' + art_item_k + '] = ' + art_item_v)

    if listitem._info:
        for info_item_k, info_item_v in listitem._info.items():
            print('    - [' + info_item_k + '] = ' + repr(info_item_v))

    if listitem._stream:
        for item_k, item_v in listitem._stream.items():
            print('    - [' + item_k + '] = ' + repr(item_v))


    """
    if listitem._property:
        for property_item_k, property_item_v in listitem._property.items():
            print('    - [' + property_item_k + '] = ' + repr(property_item_v))
    """


    print('')
