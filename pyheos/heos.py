#!/usr/bin/env python3
"""
Python bindings for Denon HEOS
"""

import asyncio
import json
from .constants import HEOS_PORT, HEOS_ST_NAME, HEOS_USERNAME, HEOS_PASSWORD, COMMAND_REGISTRY, HEOS_CACHETIME

class HEOSException(Exception):
    """ Generic HEOS Exception class """

    def __init__(self, errid, message):
        self.message = message
        self.errorid = errid


class HEOS(object):
    """ Generic class for a HEOS system """

    def __init__(self, loop, host=None, port=None):
        from datetime import datetime
        self._host = host
        self._port = port
        self._loop = loop
        self._refresh_groups = datetime(1970, 1, 1)
        self._refresh_players = datetime(1970, 1, 1)
        self._groups = {}
        self._players = {}


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
            url = self._filter_ssdp_response(responses=discover(), st=HEOS_ST_NAME)
            self._host = self._url_converter(url)

        yield from self._connect(self._host, port)

        # We are now connected. Let's initialize.
        # CLI 2.1.1
        self.register_for_events(register=False)
        self.sign_in(username=HEOS_USERNAME, password=HEOS_PASSWORD)
        self.get_heos_state(force_refresh=True)
        self.register_for_events()
        if self._subscription_task is None:
            self._subscription_task = self._loop.create_task(self._subscribe(callback))

    @asyncio.coroutine
    def _connect(self, host, port):
        """ Perform legwork for connections """
        while True:
            try:
                self._reader, self._writer = yield from asyncio.open_connection(host, port, self._loop)
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
            if response.st == st:
                return response.location

    def send_command(self, command, payload=None):
        """ Sends a command to a known destination """
        message = 'heos://' + str(command)
        if payload:
            message += '?' + '&'.join("{}={}".format(k, v) for (k, v) in payload.items())

        self._writer.write(message.encode('ascii'))

    def register_for_events(self, register=True):
        """ Sets up callback handler for events"""
        if not register:
            payload = 'off'
        else: payload = 'on'

        self.send_command(COMMAND_REGISTRY['CMD_REGISTER_CHANGE_EVENTS'], {'enable': payload})

    def sign_in(self, username, password):
        """ Sign in to the given HEOS account """
        raise NotImplementedError

    def get_heos_state(self, force_refresh=False):
        """ Request complete state from HEOS system """
        self._groups = self.get_groups(force_refresh)
        self._players = self.get_players(force_refresh)
        for group in self._groups:
            self._groupinfo[group['id']] = self.get_group_info(group['id'], force_refresh)
        for player in self._players:
            self._playerinfo[player['id']] = self.get_player_info(player['id'], force_refresh)


    @asyncio.coroutine
    def _subscribe(self, callback=None):
        """ Perform subscription to events and construct event loop """
        while True:
            if self._reader is None:
                yield from asyncio.sleep(0.1)
                continue

            try:
                incoming = yield from self._reader.readline()

            except (ConnectionResetError, TimeoutError):
                # Reconnect
                yield from self._connect(self._host, self._port)

            command = json.loads(incoming.decode())

            try:
                self._parse_event(command)

            except HEOSException as e:
                continue

            if callback:
                self._loop.create_task(self._perform_callback(callback))

    def _handle_command(self, *args, **kwargs):
        """ Generic wrapper to handle outgoing commands """
        raise NotImplementedError

    def _parse_event(self, *args, **kwargs):
        """ Parse event message """

    def get_groups(self, force_refresh=False):
        """ Get group info """

        from datetime import datetime

        now = datetime.now()

        if force_refresh:
            self.send_command(COMMAND_REGISTRY['CMD_GET_GROUPS'])
        elif self._refresh_groups and now - self._refresh_groups < HEOS_CACHETIME:
            # Not sending the command since we're in the cache lifetime
            pass
        else:
            self.send_command(COMMAND_REGISTRY['CMD_GET_GROUPS'])

    def get_players(self, force_refresh=False):
        """ Get player info """

        from datetime import datetime

        now = datetime.now()

        if force_refresh:
            self.send_command(COMMAND_REGISTRY['CMD_GET_PLAYERS'])
        elif self._refresh_players and now - self._refresh_players < HEOS_CACHETIME:
            # Not sending the command since we're in the cache lifetime
            pass
        else:
            self.send_command(COMMAND_REGISTRY['CMD_GET_PLATERS'])

    @asyncio.coroutine
    def _perform_callback(self, callback=None):
        """ Execute callback """
        if callback:

