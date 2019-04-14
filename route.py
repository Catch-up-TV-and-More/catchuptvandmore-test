# -*- coding: utf-8 -*-

from directory import Item

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


class Route:

    # Explorer routes
    # - type: list<str(path)>
    _explored_paths = set()

    # Routes to explore (Route)
    # - type: list<Route>
    _exploring_routes = []

    current_explored_route = None

    @classmethod
    def continue_epxloration(cls):
        if len(cls._exploring_routes) == 0:
            return False
        return True

    @classmethod
    def previous_route(cls):
        cls._exploring_routes.pop()

    @classmethod
    def add_route_to_explore(cls, route):
        cls._exploring_routes.append(route)

    @classmethod
    def add_item_to_explore(cls, item):
        item_label = item.get_label()
        item_base_url = item.get_base_url()
        item_query_string = item.get_query_string()
        item_path = list(cls.current_explored_route.path)
        item_path.append(item.key)

        cls._exploring_routes.append(Route(
            label=item_label,
            base_url=item_base_url,
            query_string=item_query_string,
            path=item_path))

    @classmethod
    def get_route_to_explore(cls):
        route = cls._exploring_routes[-1]
        cls.current_explored_route = route
        cls._explored_paths.add(str(route.path))
        return route

    @classmethod
    def pretty_exploring_routes(cls):
        path_pp = LEFT_ARROW_CURVING_RIGHT + ' '
        cnt = 0
        for route in Route._exploring_routes:
            if cnt != 0:
                path_pp += ' ' + RIGHT_ARROW + ' '
            path_pp += route.label + ' (' + str(route.path[-1]) + ')'
            cnt += 1
        return path_pp

    def __init__(self, label='', base_url='plugin://plugin.video.catchuptvandmore/', query_string='', path=[]):
        self.path = path
        self.label = label
        self.base_url = base_url
        self.process_handle = '1'
        if query_string != '':
            query_string = '?' + query_string
        self.query_string = query_string

    def __str__(self):
        s = '* {} - {} - {}{}'.format(self.label, self.path, self.base_url, self.query_string)
        return s

    def get_fake_sys_argv(self):
        fake_sys_argv = [
            self.base_url,
            self.process_handle,
            self.query_string
        ]
        return fake_sys_argv




