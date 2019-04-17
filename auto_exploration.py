# -*- coding: utf-8 -*-

from config import Config
from random import randint


class AutoExploration:

    # - key: str(path)
    # - value: list<int>
    items_to_explore = {}

    explored_items_cnt = 0

    @classmethod
    def add_items_current_menu(cls, current_path, current_menu_items):

        # If current_path alredy in items_to_explore, nothing to do
        if str(current_path) in cls.items_to_explore:
            print('[DEBUG add items current menu auto exploration] Menu items already added --> return')
            return

        # Is max depth reached nothing to do
        if len(current_path) >= Config.get('max_depth') and \
                Config.get('max_depth') != -1:
            print('[DEBUG add items current menu auto exploration] Max depth reached --> return')
            return


        # Else we can add items to explore

        # Firstly we create our iterator accroding to the config
        max_index = len(current_menu_items)
        if Config.get('max_items_per_menu') != -1 and Config.get('max_items_per_menu') < max_index:
            max_index = Config.get('max_items_per_menu')

        if Config.get('exploration_strategy') == 'FIRST':
            iterator = reversed(range(1, max_index + 1))

        elif Config.get('exploration_strategy') == 'LAST':
            iterator = range(len(current_menu_items) - max_index + 1, len(current_menu_items) + 1)

        elif Config.get('exploration_strategy') == 'RANDOM':
            iterator = []
            while len(iterator) != max_index:
                r = randint(1, len(current_menu_items))
                if r not in iterator:
                    iterator.append(r)

        items_key = []
        for i in iterator:
            candidate_path = list(current_path)
            candidate_path.append(i)
            if candidate_path in Config.get('exclude_paths'):
                print('[DEBUG add items current menu auto exploration] Do not add item {} to explore because it is in exclude list'.format(i))
            else:
                print('[DEBUG add items current menu auto exploration] Add item {} to explore'.format(i))
                items_key.append(i)

        cls.items_to_explore[str(current_path)] = items_key


    @classmethod
    def next_item_to_explore(cls, current_path):

        # If max items to explore reached
        if cls.explored_items_cnt >= Config.get('max_items_to_explore') and \
                Config.get('max_items_to_explore') != -1:
            print('[DEBUG next item auto exploration] Max items number to explore reached --> -1')
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
            print('[DEBUG next item auto exploration] Max depth reached --> 0')
            return 0


        # If the current path to explore is empty
        if str(current_path) in cls.items_to_explore and \
                cls.items_to_explore[str(current_path)] == []:

            print('[DEBUG next item auto exploration] Menu all items done --> 0')
            return 0

        item_to_explore = cls.items_to_explore[str(current_path)][-1]
        cls.items_to_explore[str(current_path)].pop()
        print('[DEBUG next item auto exploration] Menu not all items done --> ' + str(item_to_explore))
        cls.explored_items_cnt += 1
        return item_to_explore

