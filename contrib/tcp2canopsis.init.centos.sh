#!/bin/bash
#
# chkconfig:
# description: Canopsis connector listening for event over TCP

### BEGIN INIT INFO
# Provides: tcp2canopsis
# Required-Start: 
# Required-Stop: 
# Should-Start: 
# Should-Stop: 
# Default-Start: 
# Default-Stop: 
# Short-Description: Canopsis connector listening for event over TCP
# Description: Canopsis connector listening for event over TCP     
### END INIT INFO

# Source function library.
. /etc/init.d/functions

CONNECTOR_DIR="/usr"  # Must be defined in /etc/sysconfig/tcp2canopsis
PROG="tcp2canopsis"

[ -e /etc/sysconfig/$PROG ] && . /etc/sysconfig/$PROG

start() {
    echo -n "Starting $PROG: "
    daemon $CONNECTOR_DIR/bin/$PROG -c $CONNECTOR_DIR/$PROG.conf &
    retval=$?
    [ $retval -eq 0 ] && touch /var/lock/subsys/$PROG
    echo
    return $retval
}   

stop() {
    echo -n "Shutting down $PROG: "
    killproc $PROG
    retval=$?
    [ $retval -eq 0 ] && rm -f /var/lock/subsys/$PROG
    echo
    return $retval
}

case "$1" in
    start) start ;;
    stop) stop ;;
    status) status $PROG ;;

    restart)
        stop
        start
    ;;

    *)
        echo "Usage: $PROG {start|stop|status|restart}"
        exit 1
    ;;
esac

exit $?
