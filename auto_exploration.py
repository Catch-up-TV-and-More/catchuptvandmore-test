# -*- coding: utf-8 -*-

from config import Config
from random import randint


class AutoExploration:

    # - key: str(path)
    # - value: list<int>
    items_to_explore = {}

    explored_items_cnt = 0

    @classmethod
    def add_items_current_menu(cls, current_path, current_directory):

        # If current_path alredy in items_to_explore, nothing to do
        if str(current_path) in cls.items_to_explore:
            print('[DEBUG] Menu already seen, do not add its items in stack to explore')
            return

        # Is max depth reached nothing to do
        if len(current_path) >= Config.get('max_depth') and \
                Config.get('max_depth') != -1:
            print('[DEBUG] Max depth reached, do not add menu items in stack to explore')
            return

        # If we are in update_listing mode, do not explore deeper
        if current_directory.update_listing:
            print('[DEBUG] (TEMPO?) update_listing is True, do not explore deeper')
            return



        # Else we can add items to explore

        # Firstly we create our iterator accroding to the config
        max_index = len(current_directory.items)
        if Config.get('max_items_per_menu') != -1 and Config.get('max_items_per_menu') < max_index:
            max_index = Config.get('max_items_per_menu')

        if Config.get('exploration_strategy') == 'FIRST':
            iterator = reversed(range(1, max_index + 1))

        elif Config.get('exploration_strategy') == 'LAST':
            iterator = range(len(current_directory.items) - max_index + 1, len(current_directory.items) + 1)

        elif Config.get('exploration_strategy') == 'RANDOM':
            iterator = []
            while len(iterator) != max_index:
                r = randint(1, len(current_directory.items))
                if r not in iterator:
                    iterator.append(r)

        items_key = []
        for i in iterator:
            candidate_path = list(current_path)
            candidate_path.append(i)
            if candidate_path in Config.get('exclude_paths'):
                print('[DEBUG] Do not add item {} to explore stack because it is in exclude list'.format(i))
            elif Config.get('skip_playable_items') and current_directory.items[i].is_folder is False:
                print('[DEBUG] Do not add item {} to explore stack because it is a playable item'.format(i))
            else:
                print('[DEBUG] Add item {} to explore stack'.format(i))
                items_key.append(i)

        cls.items_to_explore[str(current_path)] = items_key


    @classmethod
    def next_item_to_explore(cls, current_path, current_directory):

        # If max items to explore reached
        if cls.explored_items_cnt >= Config.get('max_items_to_explore') and \
                Config.get('max_items_to_explore') != -1:
            print('[DEBUG] Max items number to explore reached --> next_item: -1')
            return -1

        # If we are at the entry point
        if current_path == Config.get('entry_point'):
            # print('[DEBUG next item auto exploration] Entry point all items done --> -1')

            if str(current_path) in cls.items_to_explore and \
                    cls.items_to_explore[str(current_path)] == []:

                return -1

            if str(current_path) not in cls.items_to_explore:
                return -1

        # Is max depth reached, go back
        if len(current_path) >= Config.get('max_depth') and \
                Config.get('max_depth') != -1:
            print('[DEBUG] Max depth reached --> next_item: 0')
            return 0

        # If we are in update_listing mode, go back
        if current_directory.update_listing:
            print('[DEBUG] (TEMPO?) update_listing is True --> next_item: 0')
            return 0


        # If the current path to explore is empty
        if str(current_path) in cls.items_to_explore and \
                cls.items_to_explore[str(current_path)] == []:

            print('[DEBUG] All items of this menu was expored --> next_item: 0')
            return 0

        item_to_explore = cls.items_to_explore[str(current_path)][-1]
        cls.items_to_explore[str(current_path)].pop()
        print('[DEBUG] Not all items of this menu was explored --> next_item: {}'.format(item_to_explore))
        cls.explored_items_cnt += 1
        return item_to_explore
