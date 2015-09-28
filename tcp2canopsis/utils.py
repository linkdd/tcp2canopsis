# -*- coding: utf-8 -*-

import threading


def setInterval(interval):
    def decorator(function):
        def wrapper(*args, **kwargs):
            stopped = threading.Event()

            # executed in another thread
            def loop():
                # until stopped
                while not stopped.wait(interval):
                    function(*args, **kwargs)

            t = threading.Thread(target=loop)
            # stop if the program exits
            t.daemon = True
            t.start()

            return stopped

        return wrapper

    return decorator
