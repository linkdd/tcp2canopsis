# -*- coding: utf-8 -*-

from twisted.internet import protocol


class ConnectorFactory(protocol.Factory):
    def __init__(self, connector):
        self.clients = set()
        self.connector

    def buildProtocol(self, addr):
        return self.connector(self, addr)
