from pyheos import HEOSException, get_message_parts
import sys


def get_players(heosobj, command, data):
    """CLI 4.2.1"""

    from datetime import datetime

    try:
        setattr(heosobj, '_players', data)
        setattr(heosobj, '_refresh_players', datetime.now())
    except:
        e = sys.exc_info()
        raise HEOSException(message=e[1] + ": " + e[2])


def get_player_info(heosobj, command, data):
    """CLI 4.2.2"""

    all_player_info = heosobj.players
    new_pid = data['pid']

    new_player_info = {}
    for player in all_player_info:
        if player['pid'] == new_pid:
            new_player_info.update(data)
        else:
            new_player_info.update(player)

    from datetime import datetime

    try:
        setattr(heosobj, '_players', new_player_info)
        setattr(heosobj, '_refresh_players', datetime.now())
    except:
        e = sys.exc_info()
        raise HEOSException(message=e[1] + ": " + e[2])


def get_play_state(heosobj, command, data):
    """CLI 4.2.3"""

    parts = get_message_parts(data)
    if 'pid' in parts.keys():
        pid = parts['pid']
    else:
        raise HEOSException(message='Response does not contain PID, aborting')

    if 'state' in parts.keys():
        state = parts['state']
    else:
        raise HEOSException(message='Response does not contain state, aborting')

    if state not in ['play', 'pause', 'stop']:
        raise HEOSException(message='Invalid play state received: {}'.format(state))

    try:
        attrname = "_play_states['" + pid + "']"
        setattr(heosobj, attrname, state)
    except:
        e = sys.exc_info()
        raise HEOSException(message=e[1] + ": " + e[2])


def set_play_state(heosobj, command, data):
    """CLI 4.2.4"""

    get_play_state(heosobj, command, data)


def get_now_playing_media(heosobj, command, data):
    """CLI 4.2.5"""

    # TODO We need to get passed message, payload AND options to handle this
    pass


def get_volume(heosobj, command, data):
    """CLI 4.2.6"""

    parts = get_message_parts(data)

    if 'pid' in parts.keys():
        pid = parts['pid']
    else:
        raise HEOSException(message='Response does not contain PID, aborting')

    if 'level' in parts.keys():
        vol_level = parts['level']
    else:
        raise HEOSException(message='Response does not contain volume level, aborting')

    try:
        attrname = "_player_volumes['" + pid + "']"
        setattr(heosobj, attrname, vol_level)
    except:
        e = sys.exc_info()
        raise HEOSException(message=e[1] + ": " + e[2])


def set_volume(heosobj, command, data):
    """CLI 4.2.7"""

    get_volume(heosobj, command, data)


def volume_up(heosobj, command, data):
    """CLI 4.2.8"""

    parts = get_message_parts(data)

    if 'pid' in parts.keys():
        pid = parts['pid']
    else:
        raise HEOSException(message='Response does not contain PID, aborting')

    if 'step' in parts.keys():
        step_level = parts['step']
    else:
        raise HEOSException(message='Response does not contain volume level, aborting')

    #TODO: Should we store this somewhere? And for which use? Or should we just get_volume?


def volume_down(heosobj, command, data):
    """CLI 4.2.9"""

    volume_up(heosobj, command, data)


def get_mute(heosobj, command, data):
    """CLI 4.2.10"""

    parts = get_message_parts(data)

    if 'pid' in parts.keys():
        pid = parts['pid']
    else:
        raise HEOSException(message='Response does not contain PID, aborting')

    if 'state' in parts.keys():
        state = parts['state']
    else:
        raise HEOSException(message='Response does not contain state, aborting')

    if state not in ['on', 'off']:
        raise HEOSException(message='Illegal state received: {}'.format(state))

    try:
        attrname = "_player_mute['" + pid + "']"
        setattr(heosobj, attrname, state)
    except:
        e = sys.exc_info()
        raise HEOSException(message=e[1] + ": " + e[2])
