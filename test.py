# -*- coding: utf-8 -*-

from tcp2canopsis.factory import ConnectorFactory
from tcp2canopsis.errors import ConnectorError
from tcp2canopsis.connector import Connector
from tcp2canopsis.daemon import Application
import unittest
import logging
import json


class TestTCP2Canopsis(unittest.TestCase):
    def setUp(self):
        self.event = {
            'connector': 'unittest',
            'connector_name': 'tcp2canopsis',
            'event_type': 'check',
            'source_type': 'resource',
            'component': 'connector',
            'resource': 'test',
        }
        self.eventjson = json.dumps(self.event)

        self.amqpuri = 'amqp://'
        self.token = 'testToken'
        self.realroute = 'amqp'

        self.factory = ConnectorFactory(self.amqpuri, self.token, self.realroute, Connector)

        self.connector = self.factory.buildProtocol('noaddress')
        self.connector.send_event = lambda rk, event: None

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
        rk = self.connector.generate_rk(self.event)

        self.assertEqual(
            'unittest.tcp2canopsis.check.resource.connector.test',
            rk
        )

    def test_connector_generate_rk_fail(self):
        with self.assertRaises(ConnectorError):
            self.connector.generate_rk({})

    def test_connector_tryAuthentication_fail(self):
        with self.assertRaises(ConnectorError):
            self.connector.tryAuthentication('')

    def test_connector_not_isAuthenticated(self):
        self.assertFalse(self.connector.isAuthenticated())

    def test_connector_isAuthenticated(self):
        self.connector.tryAuthentication(self.token)
        self.assertTrue(self.connector.isAuthenticated())

    def test_connector_processLine(self):
        self.connector.processLine(self.eventjson)

    def test_connector_processLine_fail(self):
        with self.assertRaises(ConnectorError):
            self.connector.processLine('')

    def test_connector_processLine_exists(self):
        self.assertTrue(hasattr(self.connector, 'processLine'))

    def test_connector_processLine_devnull(self):
        self.connector.factory.realroute = 'devnull'
        self.assertEqual(self.connector.getRealRoute(), self.connector.processLineDevNull)

    def test_connector_processLine_amqp(self):
        self.connector.factory.realroute = 'amqp'
        self.assertEqual(self.connector.getRealRoute(), self.connector.processLineAMQP)

    def test_connector_processLine_default(self):
        self.connector.factory.realroute = None
        self.assertEqual(self.connector.getRealRoute(), self.connector.processLineAMQP)

    def test_daemon_config_fail(self):
        with self.assertRaises(RuntimeError):
            Application({})

    def test_daemon_config(self):
        app = Application({
            'port': 8000,
            'amqp': 'amqp://',
            'token': 'test',
        })

        self.assertEqual(8000, app.config.get('port', None))
        self.assertEqual('amqp://', app.config.get('amqp', None))
        self.assertEqual('test', app.config.get('token', None))
        self.assertEqual(None, app.config.get('ssl-cert', None))
        self.assertEqual(None, app.config.get('ssl-key', None))

        self.assertFalse(app.ssl)
        self.assertEqual('tcp:8000', app.server)

    def test_daemon_config_ssl(self):
        app = Application({
            'port': 8000,
            'amqp': 'amqp://',
            'token': 'test',
            'ssl-cert': 'cert.pem',
            'ssl-key': 'key.pem'
        })

        self.assertEqual(8000, app.config.get('port', None))
        self.assertEqual('amqp://', app.config.get('amqp', None))
        self.assertEqual('test', app.config.get('token', None))
        self.assertEqual('cert.pem', app.config.get('ssl-cert', None))
        self.assertEqual('key.pem', app.config.get('ssl-key', None))

        self.assertTrue(app.ssl)
        self.assertEqual(
            'ssl:8000:privateKey=key.pem:certKey=cert.pem',
            app.server
        )


if __name__ == '__main__':
    logger = logging.getLogger('tcp2canopsis')
    logger.addHandler(logging.NullHandler())

    unittest.main()
