# -*- coding: utf-8 -*-

from tcp2canopsis.errors import ConnectorError
from tcp2canopsis.connector import send_event
from tcp2canopsis.utils import setInterval


class Cache(object):
    def __init__(self, factory, cache_time, *args, **kwargs):
        super(Cache, self).__init__(*args, **kwargs)

        self.factory = factory
        self.events = {}

        decorator = setInterval(cache_time)
        emitter = decorator(self.emit)
        self.stop = emitter()

    def __getitem__(self, rk):
        if rk not in self.events:
            self.events[rk] = []

        return self.events[rk]

    def __setitem__(self, rk, event):
        if rk not in self.events:
            self.events[rk] = []

        self.events[rk].append(event)

    def emit(self):
        for rk in self.events:
            if len(self.events[rk]) > 0:
                self.factory.logger.info(u'Emit: {0}'.format(rk))

                event = self.events[rk].pop(0)

                try:
                    send_event(self.factory, rk, event)

                except ConnectorError as err:
                    self.factory.log_exception(err)
