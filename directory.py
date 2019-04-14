# -*- coding: utf-8 -*-

import imghdr
import urlquick

from config import Config


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
QUESTION_MARK = u'\U00002754'



def check_image(path):
    # First we need to check if image is local or from internet
    image_pp = ''

    if 'http' in path:
        image_pp += WEB + ' '

        if not Config.get('disable_image_check'):
            # We need to check the status code without download the image
            r = urlquick.head(path)
            if 'image' in r.headers['content-type']:
                image_pp += CHECK
            else:
                image_pp += NO_CHECK
        else:
            image_pp += QUESTION_MARK

    else:
        image_pp += COMPUTER + ' '
        try:
            result = imghdr.what(path)
            if result is None:
                image_pp += NO_CHECK
            else:
                if path == Config.get('addon_icon_filepath'):
                    image_pp += TV
                elif path == Config.get('addon_fanart_filepath'):
                    image_pp += TV
                else:
                    image_pp += CHECK
        except Exception:
            image_pp += NO_CHECK

    return image_pp


def compute_column_size(column):
    if column == 'label':
        return int(Config.get('console_size') / 5)
    if column == 'plot':
        return int(Config.get('console_size') / 4)
    raise Exception(
        'Unknown column name: {}'.format(column))


def truncate_string(column, string):
    max_size = compute_column_size(column) - 1
    string_len = len(string)

    result = string
    if string_len > max_size:
        last_chars = string[-4:]
        first_chars = string[:max_size - 8]
        result = first_chars + '...' + last_chars

    return result


class Item():

    def __init__(self, url='', listitem=None, is_folder=False, key=0):
        self.url = url
        self.listitem = listitem
        self.is_folder = is_folder
        self.key = key

    def get_label(self):
        return self.listitem.getLabel()

    def get_query_string(self):
        splitted_url = self.url.split('?')
        return splitted_url[1]

    def get_base_url(self):
        splitted_url = self.url.split('?')
        return splitted_url[0]


    def format_item(self, cnt):
        listitem = self.listitem
        is_folder = self.is_folder
        url = self.url

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
            plot_pp = truncate_string('plot', (listitem._info['video']['plot']))
            plot_pp = plot_pp.replace('\n', ' ').replace('\r', '')

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



class Directory():

    current_directory = None

    @classmethod
    def is_current_directory_playable(cls):
        if len(cls.current_directory.items) == 1 and \
                cls.current_directory.items[0].is_folder is False:
            return True
        return False

    def __init__(self, succeeded=False, update_listing=False, path=[]):
        self.items = {}
        self.succeeded = succeeded
        self.update_listing = update_listing
        self.path = path



    def __str__(self):
        dash = '-' * Config.get('console_size')

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

        if len(Directory.current_directory.path) > 1:
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
        for key, item in Directory.current_directory.items.items():
            cnt += 1
            listing_array.append(item.format_item(cnt))


        s = '\n'
        for i in range(len(listing_array)):

            if i == 0:
                s += dash + '\n'

            s += '{:{key_size}}{:{type_size}}{:{label_size}} {:{plot_size}} {:{duration_size}}{:{date_size}}{:{thumb_size}}{:{fanart_size}}\n'.format(
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
            )

            if i == 0:
                s += dash + '\n'
        s += '\n'
        return s


