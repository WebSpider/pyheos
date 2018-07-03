#!/usr/bin/env python3
"""
Python bindings for Denon HEOS
"""

import asyncio

class HEOSException(Exception):
    """ Generic HEOS Exception class """

    def __init__(self, errid, message):
        self.message = message
        self.errorid = errid


class HEOS(object):
    """ Generic class for a HEOS system """

    def __init__(self):
        self._host = None
        self._port = None

    async def connect(self, host=None, port=None, callback=None):
        """ Connect to HEOS """

        if host is not None:
            self._host = host

        if port is not None:
            self._port = port

        yield from self._connect(self, host, port)

    async def _connect(self, host, port):
        """ Perform legwork for connections """
        while True:
            self._reader, self._writer = yield from asyncio.open_connection(host=host, port=port)
            return

