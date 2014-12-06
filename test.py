# -*- coding: utf-8 -*-

from tcp2canopsis.factory import ConnectorFactory
from tcp2canopsis.errors import ConnectorError
from tcp2canopsis.connector import Connector
import unittest


class TestTCP2Canopsis(unittest.TestCase):
    def setUp(self):
        self.amqpuri = 'amqp://'
        self.factory = ConnectorFactory(self.amqpuri, Connector)
        self.connector = self.factory.buildProtocol(None)

    def tearDown(self):
        del self.factory
        del self.connector

    def test_factory_buildProtocol(self):
        self.assertTrue(isinstance(self.connector, Connector))
        self.assertIs(self.connector.factory, self.factory)

    def test_connector_connection(self):
        self.connector.connectionMade()
        self.assertTrue(self.connector in self.factory.clients)

        self.connector.connectionLost(None)
        self.assertFalse(self.connector in self.factory.clients)

    def test_connector_parse_event(self):
        event = self.connector.parse_event('{"foo": "bar"}')
        self.assertTrue(isinstance(event, dict))
        self.assertEqual('bar', event.get('foo', None))

    def test_connector_parse_event_fail(self):
        with self.assertRaises(ConnectorError):
            self.connector.parse_event('{"foo":')

    def test_connector_generate_rk(self):
        event = {
            'connector': 'unittest',
            'connector_name': 'tcp2canopsis',
            'event_type': 'check',
            'source_type': 'resource',
            'component': 'connector',
            'resource': 'generate_rk',
        }
        rk = self.connector.generate_rk(event)

        self.assertEqual(
            'unittest.tcp2canopsis.check.resource.connector.generate_rk',
            rk
        )

    def test_connector_generate_rk_fail(self):
        with self.assertRaises(ConnectorError):
            self.connector.generate_rk({})


if __name__ == '__main__':
    unittest.main()