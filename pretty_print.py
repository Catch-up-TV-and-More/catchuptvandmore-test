# -*- coding: utf-8 -*-

from config import CONFIG
import runtime
import common

import imghdr
import urlquick

RIGHT_ARROW = u'\U000027A1'
LEFT_ARROW = u'\U00002B05'
FOLDER = u'\U0001F4C1'
PLAY = u'\U000025B6'
SQUARE = u'\U000025FD'
WEB = u'\U0001F30D'
COMPUTER = u'\U0001F5A5'
CHECK = u'\U00002705'
NO_CHECK = u'\U0000274C'
RED_RING = u'\U00002B55'
TV = u'\U0001F4FA'
WARNING = u'\U000026A0'
BACK_ARROW = u'\U0001F519'
LEFT_ARROW_CURVING_RIGHT = u'\U000021AA'


def check_image(path):
    # First we need to check if image is local or from internet
    from_internet = False
    valid_image = True
    is_addon_icon = False
    is_addon_fanart = False

    if 'http' in path:
        from_internet = True

        # We need to download it and check it
        # TODO Do not download picture but just check return code
        r = urlquick.get(path)
        if r.status_code != 200:
            valid_image = False
        else:
            # Tempo avant de vérifier avec imghr
            pass

    else:
        try:
            result = imghdr.what(path)
            if result is None:
                valid_image = False
            else:
                if path == common.ADDON_ICON_PATHFILE:
                    is_addon_icon = True
                elif path == common.ADDON_FANART_PATHFILE:
                    is_addon_fanart = True
                else:
                    pass
        except Exception:
            valid_image = False

    image_pp = ''

    if from_internet:
        image_pp += WEB
    else:
        image_pp += COMPUTER

    image_pp += ' '

    if is_addon_icon or is_addon_fanart:
        image_pp += TV
    elif valid_image:
        image_pp += CHECK
    else:
        image_pp += NO_CHECK

    return image_pp


def truncate_string(column, string):
    max_size = compute_column_size(column) - 1
    string_len = len(string)

    result = string
    if string_len > max_size:
        last_chars = string[-4:]
        first_chars = string[:max_size - 8]
        result = first_chars + '...' + last_chars

    return result


def compute_column_size(column):
    if column == 'label':
        return int(CONFIG['console_size'] / 5)
    if column == 'plot':
        return int(CONFIG['console_size'] / 4)
    raise Exception(
        'Unknown column name: ' + column)


def format_item(item, cnt):
    listitem = item['listitem']
    is_folder = item['is_folder']
    url = item['url']

    # Type
    type_pp = SQUARE
    if is_folder:
        type_pp = FOLDER
    elif 'isplayable' in listitem._property and listitem._property['isplayable'] == 'true':
        type_pp = PLAY

    # Label
    label_pp = truncate_string('label', listitem.getLabel())

    # Plot
    plot_pp = ''
    if 'video' in listitem._info and 'plot' in listitem._info['video']:
        plot_pp = truncate_string('plot', listitem._info['video']['plot'])

    # Thumb
    thumb_pp = ''
    if 'thumb' in listitem._art:
        thumb_pp = check_image(listitem._art['thumb'])
    else:
        thumb_pp = RED_RING

    # Fanart
    fanart_pp = ''
    if 'fanart' in listitem._art:
        fanart_pp = check_image(listitem._art['fanart'])
    else:
        fanart_pp = RED_RING

    # Duration
    duration_pp = ''
    if 'video' in listitem._info and 'duration' in listitem._info['video']:
        duration_sec = listitem._info['video']['duration']
        if duration_sec < 60:
            duration_pp = str(duration_sec) + ' s'
        else:
            hours = duration_sec // 3600
            duration_sec = duration_sec - (hours * 3600)
            minutes = duration_sec // 60
            seconds = duration_sec - (minutes * 60)
            if hours == 0:
                duration_pp = str(minutes) + ':' + str(seconds)
            else:
                duration_pp = str(hours) + ':' + str(minutes) + ':' + str(seconds)

    # Date
    date_pp = ''
    if 'video' in listitem._info and 'date' in listitem._info['video']:
        date_pp = listitem._info['video']['date']


    '''
    if listitem._label2:
        print('    - [label2] = ' + listitem._label2)

    print('Art')

    if listitem._art:
        for art_item_k, art_item_v in listitem._art.items():
            print('    - [' + art_item_k + '] = ' + art_item_v)


    print('Info')
    if listitem._info:
        for info_item_k, info_item_v in listitem._info.items():
            print('    - [' + info_item_k + '] = ' + repr(info_item_v))


    print('Stream')
    if listitem._stream:
        for item_k, item_v in listitem._stream.items():
            print('    - [' + item_k + '] = ' + repr(item_v))


    print('Property')
    if listitem._property:
        for property_item_k, property_item_v in listitem._property.items():
            print('    - [' + property_item_k + '] = ' + repr(property_item_v))
    '''

    return {
        'key': str(cnt),
        'type': type_pp,
        'label': label_pp,
        'plot': plot_pp,
        'thumb': thumb_pp,
        'fanart': fanart_pp,
        'duration': duration_pp,
        'date': date_pp
    }


def print_formated_listing(items):
    dash = '-' * CONFIG['console_size']

    listing_array = []

    first_line = {
        'key': '',
        'type': '',
        'label': 'Label',
        'plot': 'Plot',
        'thumb': 'Thumb',
        'fanart': 'Fanart',
        'duration': 'Time',
        'date': 'Date'

    }

    listing_array.append(first_line)

    if len(runtime.CURRENT_PATH) > 1:
        previous_line = {
            'key': str(0),
            'type': LEFT_ARROW,
            'label': 'Previous menu',
            'plot': '',
            'thumb': '',
            'fanart': '',
            'duration': '',
            'date': ''
        }
        listing_array.append(previous_line)

    cnt = 0
    for item in items:
        cnt += 1
        listing_array.append(format_item(item, cnt))

    print('')
    for i in range(len(listing_array)):

        if i == 0:
            print(dash)

        print('{:{key_size}}{:{type_size}}{:{label_size}} {:{plot_size}} {:{duration_size}}{:{date_size}}{:{thumb_size}}{:{fanart_size}}'.format(
            listing_array[i]['key'],
            listing_array[i]['type'],
            listing_array[i]['label'],
            listing_array[i]['plot'],
            listing_array[i]['duration'],
            listing_array[i]['date'],
            listing_array[i]['thumb'],
            listing_array[i]['fanart'],
            key_size=3,
            type_size=4,
            label_size=compute_column_size('label'),
            plot_size=compute_column_size('plot'),
            thumb_size=6,
            fanart_size=6,
            duration_size=8,
            date_size=12
        ))

        if i == 0:
            print(dash)

    print('')


def current_path_pp(path):
    path_pp = LEFT_ARROW_CURVING_RIGHT + ' '
    cnt = 0
    for i in path:
        if cnt != 0:
            path_pp += ' ' + RIGHT_ARROW + ' '
        path_pp += i['label'] + ' (' + str(i['key']) + ')'
        cnt += 1
    return path_pp


def print_encountered_errors():
    if runtime.ALL_REPORTED_ERROR:
        print('')
        print('Encountered errors list:')
        cnt = 0
        for error in runtime.ALL_REPORTED_ERROR:
            print('\n\t* Error ', cnt)
            print('\t\t- Type: ', error['type'])
            print('\t\t- Parent path: ', error['path'])
            print('\t\t- Route: ', error['route'])
            print('\t\t- Params: ', error['params'])

            cnt += 1
