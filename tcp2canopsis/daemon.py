# -*- coding: utf-8 -*-

from tcp2canopsis.factory import ConnectorFactory
from tcp2canopsis.connector import Connector
from twisted.internet import reactor, endpoints

from validictory.validator import FieldValidationError
from validictory.validator import RequiredFieldValidationError
from validictory import validate


class Application(object):
    SCHEMA = {
        'type': 'object',
        'properties': {
            'port': {'type': 'integer', 'required': True},
            'amqp': {'type': 'string', 'required': True},
            'token': {'type': 'string', 'required': False},
            'ssl-cert': {'type': 'string', 'required': False},
            'ssl-key': {'type': 'string', 'required': False},
            'realroute': {'type': 'string', 'required': False},
            'cache_time': {'type': 'integer', 'required': False}
        }
    }

    def __init__(self, config, *args, **kwargs):
        super(Application, self).__init__(*args, **kwargs)

        try:
            validate(config, self.SCHEMA)

        except FieldValidationError as err:
            raise RuntimeError('Invalid configuration: {0}'.format(err))

        except RequiredFieldValidationError as err:
            raise RuntimeError('Missing required parameter: {0}'.format(err))

        self.config = config
        self.ssl = 'ssl-cert' in self.config and 'ssl-key' in self.config
        self.realroute = self.config.get('realroute', 'amqp')

    @property
    def server(self):
        if self.ssl:
            return 'ssl:{0}:privateKey={1}:certKey={2}'.format(
                self.config['port'],
                self.config['ssl-key'],
                self.config['ssl-cert']
            )

        else:
            return 'tcp:{0}'.format(self.config['port'])

    def __call__(self):
        factory = ConnectorFactory(
            self.config['amqp'],
            self.config.get('token', None),
            self.realroute,
            self.config.get('cache_time', 5),
            Connector
        )

        endpoint = endpoints.serverFromString(reactor, self.server)
        endpoint.listen(factory)
        reactor.run()
