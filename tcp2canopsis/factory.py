# -*- coding: utf-8 -*-

from tcp2canopsis.cache import Cache
from twisted.internet import protocol
import logging


class ConnectorFactory(protocol.Factory):
    def __init__(self, amqpuri, token, realroute, cache_time, connector):
        self.clients = set()
        self.connector = connector
        self.amqpuri = amqpuri
        self.token = token
        self.realroute = realroute

        self.cache = Cache(self, cache_time)

        self.logger = logging.getLogger('tcp2canopsis')
        self.logger.setLevel(logging.DEBUG)

    def log_exception(self, err):
        self.logger.error('Error: {0}'.format(err))

    def buildProtocol(self, addr):
        return self.connector(self, addr)
