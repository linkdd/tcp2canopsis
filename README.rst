TCP to Canopsis connector
=========================

.. image:: https://travis-ci.org/linkdd/tcp2canopsis.svg?branch=master


This package provides a connector which listen for events on a TCP port.

Usage
-----

Run the script on a designated port (``8000`` in this example) and with the URL
of the AMQP server:

.. code-block::

   $ tcp2canopsis -p 8000 -a "amqp://guest:guest@localhost:5672/" -t token

Then use ``telnet`` to publish events:

.. code-block::

   $ telnet localhost 8000
   Trying ::1...
   Connected to localhost.
   Escape character is '^]'.
   token
   {"connector": "test", "connector_name": "testname", "event_type": "check", "source_type": "resource", "component": "testcmp", "resource": "testrsrc", "state": 0, "output": "test output"}
   {"connector": "test", "connector_name": "testname", "event_type": "check", "source_type": "resource", "component": "testcmp", "resource": "testrsrc", "state": 1, "output": "test output 2"}
   {"connector": "test", "connector_name": "testname", "event_type": "check", "source_type": "resource", "component": "testcmp", "resource": "testrsrc", "state": 0, "output": "test output 3"}
   Connection closed by foreign host.

Or in a JSON file:

.. code-block:: javascript

   {"tcp2canopsis": {
       "port": 8000,
       "amqp": "amqp://guest:guest@localhost:5672/",
       "token": "token"
   }}

And load the file using:

.. code-block::

   $ tcp2canopsis -c path/to/config.json


Configuration keys
------------------

 - ``port``: AMQP port
 - ``amqp``: AMQP URI
 - ``token``: authentication token
 - ``realroute``: ``amqp`` or ``devnull``. ``devnull`` just ignore events

SSL
---

If using configuration via command line, use those options:

.. code-block::

   $ tcp2canopsis --ssl-cert server.pem --ssl-key server.key

*NB: other options are still mandatory*

Or via the configuration file:

.. code-block:: javascript

   {"tcp2canopsis": {
       "port": 8000,
       "amqp": "amqp://guest:guest@localhost:5672/",
       "token": "token",
       "ssl-cert": "server.pem",
       "ssl-key": "server.key"
   }}

Then, instead of ``telnet``, use this command to test the connector:

.. code-block::

   $ openssl s_client -quiet -connect localhost:8000 -CAfile ca.pem -crlf
   testtoken
   {"connector": "test", "connector_name": "testname", "event_type": "check", "source_type": "resource", "component": "testcmp", "resource": "testrsrc", "state": 0, "output": "test output"}


Installation
------------

Just type:

.. code-block::

   $ pip install tcp2canopsis

Or, to install it in a locally:

.. code-block::

   $ ./makefile

This will create a virtual Python environment in the current folder, and install the dependencies listed by ``requirements.txt``.
Finally, it will perform a ``python setup.py install``.

After executing this script, the connector will be available in the current folder (which is now a virtual Python environment).

Connector on boot
-----------------

CentOS
++++++

Copy the initscript and add the configuration file:

.. code-block::

   $ cp contrib/tcp2canopsis.init.centos.sh /etc/init.d/tcp2canopsis
   $ cat > /etc/sysconfig/tcp2canopsis << "EOF"
   CONNECTOR_DIR="/path/to/tcp2canopsis/virtualenv"
   EOF

Debian
++++++

TODO

systemd
+++++++

TODO
