# -*- coding: utf-8 -*-

from twisted.protocols import basic

from kombu import Connection
from kombu.pools import producers

import json


class Connector(basic.LineReceiver):
    def __init__(self, factory, addr, amqpuri):
        self.factory = factory
        self.address = addr
        self.amqpuri = amqpuri

    def connectionMade(self):
        self.factory.clients.add(self)

    def connectionLost(self, reason):
        print('Client disconnected: {0}'.format(reason))
        self.factory.clients.remove(self)

    def lineReceived(self, line):
        # Parse event
        try:
            event = json.loads(line)

        except ValueError as err:
            print('Error: Invalid event: {0}'.format(err))
            return

        # Generate routing key
        try:
            rk = '{}.{}.{}.{}.{}'.format(
                event['connector'],
                event['connector_name'],
                event['event_type'],
                event['source_type'],
                event['component']
            )

            if event['source_type'] == 'resource':
                rk = '{}.{}'.format(rk, event['resource'])

        except KeyError as err:
            print('Error: Missing key in event: {0}'.format(err))
            return

        print('Send event: {0}'.format(rk))

        try:
            with Connection(self.amqpuri) as conn:
                with producers[conn].acquire(block=True) as producer:
                    producer.publish(
                        event,
                        serializer='json',
                        exchange='canopsis.events',
                        routing_key=rk
                    )

        except Exception as err:
            print('Error: Impossible to send event: {0}'.format(err))
