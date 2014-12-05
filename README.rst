TCP to Canopsis connector
=========================

This package provides a connector which listen for events on a TCP port.

Usage
-----

Run the script on a designated port (``8000`` in this example) :

.. code-block::

   $ tcp2canopsis 8000

Then use ``telnet`` to publish events :

.. code-block::

   $ telnet localhost 8000
   Trying ::1...
   Connected to localhost.
   Escape character is '^]'.
   {"connector": "test", "connector_name": "testname", "event_type": "check", "source_type": "resource", "component": "testcmp", "resource": "testrsrc", "state": 0, "output": "test output"}
   {"connector": "test", "connector_name": "testname", "event_type": "check", "source_type": "resource", "component": "testcmp", "resource": "testrsrc", "state": 1, "output": "test output 2"}
   {"connector": "test", "connector_name": "testname", "event_type": "check", "source_type": "resource", "component": "testcmp", "resource": "testrsrc", "state": 0, "output": "test output 3"}
   Connection closed by foreign host.

Installation
------------

Just type :

.. code-block::

   $ ./makefile

This will create a virtual Python environment in the current folder, and 
