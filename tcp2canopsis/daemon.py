# -*- coding: utf-8 -*-

from tcp2canopsis.factory import ConnectorFactory
from tcp2canopsis.connector import Connector
from twisted.internet import reactor, endpoints


def run_daemon(port):
    server = 'tcp:{0}'.format(port)

    factory = ConnectorFactory(Connector)
    endpoint = endpoints.serverFromString(reactor, server)
    endpoint.listen(factory)
    reactor.run()
