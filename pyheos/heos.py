#!/usr/bin/env python3
"""
Python bindings for Denon HEOS
"""

import asyncio
import json
from .constants import HEOS_PORT, HEOS_ST_NAME, HEOS_USERNAME, HEOS_PASSWORD, COMMAND_REGISTRY, HEOS_CACHETIME


class HEOSException(Exception):
    """ Generic HEOS Exception class """

    def __init__(self, message, errid=0):
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
        self._play_states = {}
        self._heos_username = ""
        self._account_status = ""
        self._last_heartbeat = datetime(1970, 1, 1)
        self._register_for_change_events = False
        self._prettify_json_response = False
        self._player_volumes = {}
        self._player_mute = {}
        self._queue = []
        self._quickselects = []
        self._update_status = ""
        self.groups = self._groups

    @asyncio.coroutine
    def connect(self, host=None, port=HEOS_PORT, callback=None):
        """ Connect to HEOS """

        if host is not None:
            self._host = host

        if port is not None:
            self._port = port

        # Perform discovery if needed
        if not self._host:
            from .ssdp import discover
            url = self._filter_ssdp_response(responses=discover(service=HEOS_ST_NAME), st=HEOS_ST_NAME)
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
        else:
            payload = 'on'

        self.send_command(COMMAND_REGISTRY['CMD_REGISTER_CHANGE_EVENTS'], {'enable': payload})

    def sign_in(self, username, password):
        """ Sign in to the given HEOS account """
        raise NotImplementedError

    def get_heos_state(self, force_refresh=False):
        """ Request complete state from HEOS system """
        self.get_groups(force_refresh)
        self.get_players(force_refresh)

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
                self._parse_command(command)

            except HEOSException as e:
                continue

            if callback:
                self._loop.create_task(self._perform_callback(callback))

    def _handle_command(self, complete_command, payload):
        """ Generic wrapper to handle commands """
        command_group, command = complete_command.split('/')
        import importlib
        module_to_import = 'pyheos.' + command_group

        try:
            myimport = importlib.import_module(module_to_import)
        except ImportError as e:
            raise

        call = getattr(myimport, command)

        retr = call(self, command, payload)

        return retr

    def _parse_command(self, command):
        """ Parse command message """
        # TODO: Fix this to handle heos/message, payload and options
        try:
            inner_section = command['heos']
            cmd = inner_section['command']
            if 'result' in inner_section.keys() and inner_section['result'] == 'fail':
                errid = inner_section['message'].split('&')[0].split('=')[1]
                raise HEOSException(errid, inner_section['message'])

            if 'payload' in command.keys():
                self._handle_command(cmd, command['payload'])

            elif 'message' in inner_section.keys():
                message = self._parse_message(inner_section['message'])
                self._handle_command(cmd, message)

            else:
                raise HEOSException(message='Incoming command incomplete. Payload and message are missing')

        except HEOSException as e:
            raise HEOSException(message='Problems were found `with command {}'.format(e))

        return None

    @staticmethod
    def _parse_message(message):
        """ Parse message section """
        try:
            return dict(element.split('=') for element in message.split('&'))

        except ValueError as e:
            return {}


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
        pass


    def save_groups(self, groups, time):
        if isinstance(groups, dict) and groups:
            setattr(self, '_groups', groups)
            setattr(self, '_refresh_groups', time)
            return True
        else:
            return False

def get_message_parts(message, parts=[]):

    found_parts = {}
    sections = {}

    elements = message.split('&')
    for element in elements:
        (k, v) = element.split('=')
        sections[k] = v

    for item in parts:
        if item in sections.keys():
            found_parts[item] = sections[item]

    return found_parts
