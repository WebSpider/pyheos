from pyheos import HEOSException, get_message_parts


def sources_changed(heosobj, command, data):
    """CLI 5.1"""

    if command == 'event/sources_changed':
        heosobj.send_command(command='browse/get_music_sources')
    else:
        raise HEOSException(message='{} is an unknown command'.format(command),errid=501)


def players_changed(heosobj, command, data):
    """CLI 5.2"""

    if command == 'event/players_changed':
        heosobj.send_command(command='player/get_players')
    else:
        raise HEOSException(message='{} is an unknown command'.format(command), errid=502)


def group_changed(heosobj, command, data):
    """CLI 5.3"""

    if command == 'event/groups_changed':
        heosobj.send_command(command='group/get_groups')
    else:
        raise HEOSException(message='{} is an unknown command'.format(command), errid=503)


def player_state_changed(heosobj, command, data):
    """CLI 5.4"""

    if command == 'event/player_state_changed':
        pid = get_message_parts(data, ['pid'])[0]

        heosobj.send_command(command='player/get_player_info?pid={}'.format(pid))
    else:
        raise HEOSException(message='{} is an unknown command'.format(command), errid=504)


