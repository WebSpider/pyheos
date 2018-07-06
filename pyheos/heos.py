#!/usr/bin/env python3
"""
Python bindings for Denon HEOS
"""

import asyncio
from .constants import HEOS_PORT, HEOS_ST_NAME, HEOS_USERNAME, HEOS_PASSWORD, COMMAND_REGISTRY

class HEOSException(Exception):
    """ Generic HEOS Exception class """

    def __init__(self, errid, message):
        self.message = message
        self.errorid = errid


class HEOS(object):
    """ Generic class for a HEOS system """

    def __init__(self, loop, host=None, port=None):
        self._host = host
        self._port = port
        self._loop = loop


    @asyncio.coroutine
    async def connect(self, host=None, port=HEOS_PORT, callback=None):
        """ Connect to HEOS """

        if host is not None:
            self._host = host

        if port is not None:
            self._port = port

        # Perform discovery if needed
        if not self._host:
            from .ssdp import discover
            url = _filter_ssdp_response(responses=discover(), st=HEOS_ST_NAME)
            self._host = self._url_converter(url)

        yield from self._connect(self._host, port)

        # We are now connected. Let's initialize.
        # CLI 2.1.1
        self.unregister_for_change_events()
        self.sign_in(username=HEOS_USERNAME, password=HEOS_PASSWORD)
        self.get_heos_state()
        self.register_for_change_events()
        if self._subscription_task is None:
            self._subscription_task = self._loop.create_task(self._async_subscribe(callback))

    @asyncio.coroutine
    async def _connect(self, host, port):
        """ Perform legwork for connections """
        while True:
            try:
                self._reader, self._writer = yield from asyncio.open_connection(host=host, port=port)
                return
            except (TimeoutError, ConnectionRefusedError):
                return

    @staticmethod
    def _url_converter(self, url):
        import re

        pieces = re.search('(https?://)([^:^/]*)[:\\d*]?(.*)?$', url)

        if pieces:
            return pieces.group(2)
        else:
            return None

    @staticmethod
    def _filter_ssdp_response(self, responses, st):
        for response in responses:
            if response.st == st
                return response.location

    def send_command(self, command, payload):
        """ Sends a command to a known destination """
        message = 'heos://' + str(command)
        if payload:
            message += '?' + '&'.join("{}={}".format(k, v) for (k, v) in payload.items())

        self._writer.write(msg.encode('ascii'))

    def unregister_for_change_events(self):
